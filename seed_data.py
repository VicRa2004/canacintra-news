import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from news.models import News, Category, Comment
from django.contrib.auth.models import User
from django.utils.text import slugify

def seed():
    # Get or create admin user
    user, _ = User.objects.get_or_create(username='admin', defaults={'is_staff': True, 'is_superuser': True})
    if _:
        user.set_password('admin123')
        user.save()

    # Create Categories
    tech, _ = Category.objects.get_or_create(name='Tecnología', defaults={'description': 'Lo último en tech.'})
    econ, _ = Category.objects.get_or_create(name='Economía', defaults={'description': 'Noticias económicas.'})
    ind, _ = Category.objects.get_or_create(name='Industria', defaults={'description': 'Sector industrial.'})

    # Create News
    news1, _ = News.objects.get_or_create(
        title='La Revolución de la IA en la Industria',
        defaults={
            'content': '<h2>El impacto de la IA</h2><p>La inteligencia artificial está transformando la manera en que operan las fábricas modernas. Con la implementación de <strong>algoritmos avanzados</strong>, la eficiencia ha subido un 30%.</p><ul><li>Automatización inteligente</li><li>Mantenimiento predictivo</li><li>Optimización de recursos</li></ul><p>Este es un cambio de paradigma sin precedentes.</p>',
            'category': ind,
            'author': user
        }
    )

    news2, _ = News.objects.get_or_create(
        title='Crecimiento del PIB en el Primer Trimestre',
        defaults={
            'content': '<blockquote>La economía muestra señales de resiliencia ante los retos globales.</blockquote><p>El reporte del primer trimestre indica un crecimiento sostenido impulsado por las exportaciones y el consumo interno. Los analistas sugieren que esta tendencia podría continuar si las tasas de interés se mantienen estables.</p>',
            'category': econ,
            'author': user
        }
    )

    news3, _ = News.objects.get_or_create(
        title='Nuevos Avances en Semiconductores',
        defaults={
            'content': '<p>Investigadores han desarrollado un nuevo tipo de material que promete revolucionar la industria de los <i>semiconductores</i>. Este avance permitiría procesadores más rápidos y con menor consumo de energía.</p><p>Pruebas iniciales muestran una reducción del 40% en el calor generado.</p>',
            'category': tech,
            'author': user
        }
    )

    # Create Comments
    Comment.objects.get_or_create(
        news=news1,
        user=user,
        defaults={'content': 'Excelente artículo, muy informativo.', 'is_approved': True}
    )
    Comment.objects.get_or_create(
        news=news1,
        user=user,
        defaults={'content': '¿Cuándo sale la segunda parte?', 'is_approved': False}
    )

    print("Datos de prueba creados exitosamente.")

if __name__ == '__main__':
    seed()
