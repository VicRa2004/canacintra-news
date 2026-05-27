from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.db.models import Q
from .models import News, Category, Comment, NewsImage
from .forms import CommentForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView

class NewsListView(ListView):
    model = News
    template_name = 'news/news_list.html'
    context_object_name = 'news_list'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        category_slug = self.request.GET.get('category')

        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) | Q(content__icontains=query)
            )
        
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['current_category'] = self.request.GET.get('category')
        context['query'] = self.request.GET.get('q')
        context['carousel_news'] = News.objects.all()[:5]
        return context

class NewsDetailView(DetailView):
    model = News
    template_name = 'news/news_detail.html'
    context_object_name = 'news'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        context['comments'] = self.object.comments.filter(is_approved=True)
        context['related_news'] = News.objects.filter(
            category=self.object.category
        ).exclude(pk=self.object.pk).order_by('-published_at')[:4]
        return context

from django.contrib import messages

@login_required
def add_comment(request, pk):
    news = get_object_or_404(News, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.news = news
            comment.user = request.user
            comment.save()
            messages.success(request, 'Tu comentario ha sido enviado y está pendiente de aprobación.')
    return redirect('news_detail', slug=news.slug)

class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

from django.views.generic import TemplateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count
from .models import News, Category, Comment
from .forms import NewsForm, CategoryForm, NewsImageForm

class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_staff

class DashboardHomeView(StaffRequiredMixin, TemplateView):
    template_name = 'news/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Estadísticas Generales
        context['total_news'] = News.objects.count()
        context['total_comments'] = Comment.objects.count()
        context['pending_comments'] = Comment.objects.filter(is_approved=False).count()
        context['total_categories'] = Category.objects.count()
        
        # Comentarios pendientes recientes
        context['recent_pending_comments'] = Comment.objects.filter(is_approved=False).order_by('-created_at')
        
        # Categorías y noticias asociadas para listado
        context['categories_list'] = Category.objects.annotate(news_count=Count('news')).order_by('-news_count')
        
        # Todas las noticias para gestión
        context['news_list'] = News.objects.all().order_by('-published_at')
        
        # Datos para Gráfico 1: Noticias por categoría
        categories_data = Category.objects.annotate(num_news=Count('news'))
        context['chart_categories_labels'] = [c.name for c in categories_data]
        context['chart_categories_values'] = [c.num_news for c in categories_data]
        
        # Datos para Gráfico 2: Comentarios por día (últimos 7 días)
        today = timezone.now().date()
        date_labels = []
        comments_counts = []
        for i in range(6, -1, -1):
            day = today - timedelta(days=i)
            date_labels.append(day.strftime('%d %b'))
            count = Comment.objects.filter(created_at__date=day).count()
            comments_counts.append(count)
            
        context['chart_comments_labels'] = date_labels
        context['chart_comments_values'] = comments_counts
        
        # Formularios para agregar en modales
        context['category_form'] = CategoryForm()
        
        return context

from django.forms import inlineformset_factory
from django.shortcuts import redirect

NewsImageFormSet = inlineformset_factory(
    News, NewsImage,
    form=NewsImageForm,
    fields=('image', 'caption'),
    extra=1,
    can_delete=True
)

class DashboardNewsCreateView(StaffRequiredMixin, CreateView):
    model = News
    form_class = NewsForm
    template_name = 'news/dashboard_news_form.html'
    success_url = reverse_lazy('dashboard_home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['image_formset'] = NewsImageFormSet(self.request.POST, self.request.FILES)
        else:
            context['image_formset'] = NewsImageFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        image_formset = context['image_formset']
        if image_formset.is_valid():
            form.instance.author = self.request.user
            self.object = form.save()
            image_formset.instance = self.object
            image_formset.save()
            messages.success(self.request, 'El artículo se ha creado correctamente.')
            return redirect(self.get_success_url() + '?tab=news')
        else:
            return self.form_invalid(form)

class DashboardNewsUpdateView(StaffRequiredMixin, UpdateView):
    model = News
    form_class = NewsForm
    template_name = 'news/dashboard_news_form.html'
    success_url = reverse_lazy('dashboard_home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['image_formset'] = NewsImageFormSet(self.request.POST, self.request.FILES, instance=self.object)
        else:
            context['image_formset'] = NewsImageFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        image_formset = context['image_formset']
        if image_formset.is_valid():
            self.object = form.save()
            image_formset.instance = self.object
            image_formset.save()
            messages.success(self.request, 'El artículo se ha actualizado correctamente.')
            return redirect(self.get_success_url() + '?tab=news')
        else:
            return self.form_invalid(form)


class DashboardNewsDeleteView(StaffRequiredMixin, DeleteView):
    model = News
    
    def get_success_url(self):
        return reverse_lazy('dashboard_home') + '?tab=news'
    
    def post(self, request, *args, **kwargs):
        messages.success(self.request, 'El artículo se ha eliminado correctamente.')
        return super().post(request, *args, **kwargs)


@login_required
@require_POST
def approve_comment_api(request, pk):
    if not request.user.is_staff:
        return JsonResponse({'error': 'No autorizado'}, status=403)
    comment = get_object_or_404(Comment, pk=pk)
    comment.is_approved = True
    comment.save()
    return JsonResponse({'status': 'ok', 'message': 'Comentario aprobado correctamente.'})

@login_required
@require_POST
def delete_comment_api(request, pk):
    if not request.user.is_staff:
        return JsonResponse({'error': 'No autorizado'}, status=403)
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return JsonResponse({'status': 'ok', 'message': 'Comentario rechazado/eliminado correctamente.'})

@login_required
@require_POST
def create_category_api(request):
    if not request.user.is_staff:
        return JsonResponse({'error': 'No autorizado'}, status=403)
    form = CategoryForm(request.POST)
    if form.is_valid():
        category = form.save()
        return JsonResponse({
            'status': 'ok',
            'message': 'Categoría creada correctamente.',
            'category': {
                'id': category.id,
                'name': category.name,
                'description': category.description,
                'slug': category.slug
            }
        })
    else:
        return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)

