# 📰 Canacintra-2 Portal de Noticias

¡Bienvenido al repositorio de **Canacintra-2**! Este proyecto es un moderno y robusto portal de noticias desarrollado con **Django**. El sistema está diseñado para la gestión de categorías, publicación de artículos informativos, comentarios interactivos, búsquedas dinámicas y una administración moderna y visualmente atractiva.

---

## 🚀 Características Clave

- **Gestión Completa de Noticias:** Creación, edición, categorización y publicación de artículos.
- **Editor Enriquecido (WYSIWYG):** Integración de [django-ckeditor-5](https://github.com/hvlad/django-ckeditor-5) para redactar contenido con formato HTML de forma sencilla.
- **Panel de Administración Moderno:** Customizado mediante [django-unfold](https://github.com/unfoldadmin/django), ofreciendo una interfaz de administración contemporánea, intuitiva y responsive.
- **Sistema de Comentarios:** Soporte para comentarios de usuarios en las noticias, con un flujo de aprobación desde el panel de administración.
- **Diseño Premium:** Interfaz de cara al usuario final estilizada con **CSS Vanilla**, priorizando tipografías modernas, transiciones fluidas, diseño dinámico y adaptabilidad en múltiples dispositivos (UX/UI Premium).
- **Semilla de Datos:** Script para inicializar de forma rápida categorías y artículos de prueba.

---

## 🛠️ Stack Tecnológico

- **Lenguaje:** Python 3.10+
- **Framework Web:** Django 5.0.6
- **Base de Datos:** PostgreSQL
- **Estilos:** CSS Vanilla (sin frameworks pesados para un control total y excelente velocidad de carga)
- **Editor Rich Text:** CKEditor 5
- **Panel de Administración:** Unfold Admin (Tailwind-based UI para Django admin)
- **Variables de Entorno:** Manejo seguro con `python-dotenv`

---

## 📁 Estructura del Proyecto

El proyecto está organizado de la siguiente manera:

```text
canacintra-web/
│
├── core/                  # Configuración principal del proyecto Django (settings, urls, etc.)
├── news/                  # Aplicación de noticias (modelos, vistas, formularios, URLs)
├── static/                # Archivos estáticos globales (hojas de estilo CSS, scripts JS, imágenes)
│   └── css/               # Estilos personalizados (CSS Vanilla)
├── templates/             # Plantillas HTML estructuradas
├── media/                 # Archivos multimedia subidos por usuarios (portadas de noticias)
├── seed_data.py           # Script para poblar la base de datos con datos iniciales de prueba
├── requirements.txt       # Dependencias del proyecto con versiones exactas
├── .env.example           # Plantilla de variables de entorno requeridas
└── README.md              # Documentación del proyecto (este archivo)
```

---

## ⚙️ Instalación y Configuración

Sigue estos pasos para levantar el entorno de desarrollo localmente:

### 1. Requisitos Previos

Asegúrate de tener instalado en tu sistema:
- **Python 3.10+**
- **PostgreSQL** (activo y con una base de datos creada)

### 2. Entorno Virtual

Crea y activa un entorno virtual en la raíz del proyecto:

**En Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\activate
```

**En macOS/Linux:**
```bash
python -m venv venv
source venv/bin/activate
```

### 3. Instalación de Dependencias

Instala los paquetes necesarios definidos en `requirements.txt`:
```powershell
pip install -r requirements.txt
```

### 4. Variables de Entorno

Copia el archivo de ejemplo `.env.example` y renómbralo a `.env`:
```powershell
copy .env.example .env
```
Abre el archivo `.env` y edita las credenciales de PostgreSQL según la configuración de tu máquina local:
```env
DEBUG=True
SECRET_KEY=tu-clave-secreta-de-django
DB_NAME=nombre_de_tu_bd
DB_USER=usuario_de_postgres
DB_PASSWORD=contraseña_de_postgres
DB_HOST=127.0.0.1
DB_PORT=5432
```

### 5. Migraciones de la Base de Datos

Prepara e inicializa el esquema de la base de datos:
```powershell
python manage.py migrate
```

### 6. Cargar Datos de Prueba (Seed)

Para poblar rápidamente tu base de datos con categorías y noticias de prueba para interactuar inmediatamente con el sitio, ejecuta:
```powershell
python seed_data.py
```
> ⚠️ **Nota:** El script de seed creará automáticamente un usuario administrador con las siguientes credenciales:
> - **Usuario:** `admin`
> - **Contraseña:** `admin123`

Si prefieres crear un superusuario nuevo de forma manual, puedes hacerlo con:
```powershell
python manage.py createsuperuser
```

---

## 🚀 Ejecución del Servidor

Una vez configurado todo, inicia el servidor de desarrollo local de Django:

```powershell
python manage.py runserver
```

El portal estará disponible en tu navegador en:
- Sitio principal: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- Panel de Administración: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

## 📝 Reglas de Desarrollo y Buenas Prácticas

- **Idioma:** Toda documentación, explicaciones de commits y aclaraciones deben realizarse en **español**. El código fuente (nombres de variables, clases, métodos) sigue la convención en inglés/español según corresponda a las convenciones de Django.
- **Formateo de Código:** Seguir los estándares de estilo de Python (**PEP 8**).
- **Control de Versiones:** Los commits deben ser atómicos y poseer un mensaje descriptivo de la acción realizada.
- **Nuevas Dependencias:** Si se integra una biblioteca externa, debe instalarse y registrarse en `requirements.txt` utilizando **versiones exactas**.
- **Alineación de UI/UX:** Al realizar cambios visuales, se priorizan layouts limpios, modernos, fluidos y de calidad premium empleando **CSS Vanilla**. Evitar placeholders y utilizar imágenes reales o generadas.

---

## 🔍 Tareas Comunes

| Acción | Comando |
| :--- | :--- |
| **Iniciar servidor** | `python manage.py runserver` |
| **Crear nuevas migraciones** | `python manage.py makemigrations` |
| **Aplicar migraciones** | `python manage.py migrate` |
| **Crear superusuario** | `python manage.py createsuperuser` |
| **Recopilar archivos estáticos** | `python manage.py collectstatic` |
| **Cargar datos de prueba** | `python seed_data.py` |

---
*Desarrollado para la gestión informativa del portal Canacintra.*
