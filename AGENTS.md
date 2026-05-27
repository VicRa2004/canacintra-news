# Guía de Agentes - Blogy

Este documento es una guía rápida para que cualquier agente de IA o desarrollador pueda entender y colaborar en este proyecto de forma eficiente.

## 🚀 Descripción del Proyecto

**Blogy** es un portal de noticias desarrollado con **Django**. Permite la gestión de categorías, artículos de noticias, búsqueda y comentarios.

## 🛠️ Stack Tecnológico

- **Lenguaje:** Python 3.x
- **Framework:** Django 5.0.6
- **Base de Datos:** PostgreSQL
- **Estilos:** CSS Vanilla
- **Variables de Entorno:** Manejadas mediante `.env`

## 📁 Estructura del Proyecto

- `core/`: Configuración principal del proyecto (settings, urls, wsgi).
- `news/`: Aplicación principal que contiene la lógica de noticias, modelos, vistas y formularios.
- `templates/`: Plantillas HTML globales del sistema.
- `static/`: Archivos estáticos (CSS, JS, Imágenes).
- `media/`: Archivos subidos por el usuario (imágenes de noticias).
- `requirements.txt`: Dependencias del proyecto.

## ⚙️ Configuración y Ejecución

1. **Entorno Virtual:** Se recomienda usar el `venv` incluido.
   ```powershell
   .\venv\Scripts\activate
   ```
2. **Instalación de Dependencias:**
   ```powershell
   pip install -r requirements.txt
   ```
3. **Variables de Entorno:** Asegúrate de que el archivo `.env` contenga las credenciales correctas para PostgreSQL.
4. **Migraciones:**
   ```powershell
   python manage.py migrate
   ```
5. **Servidor de Desarrollo:**
   ```powershell
   python manage.py runserver
   ```

## 📝 Reglas y Buenas Prácticas

- **Idioma:** Las explicaciones y documentación deben estar en **español**.
- **Código:** Seguir estándares PEP 8 para Python.
- **Git:** Realizar commits descriptivos y atómicos.
- **Instalación de Dependencias:** Si necesitas instalar algo, usa versiones exactas.
  - Ejemplo: `pip install django==5.0.6`
- **UI/UX:** Priorizar diseños modernos, limpios y "premium" utilizando CSS vanilla y evitando placeholders (generar imágenes reales si es necesario).

## 🔍 Tareas Comunes

- **Crear Superusuario:** `python manage.py createsuperuser`
- **Crear Migraciones:** `python manage.py makemigrations`
- **Recolectar Estáticos:** `python manage.py collectstatic`
