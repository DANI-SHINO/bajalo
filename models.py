catalogo

{% extends "base.html" %}

{% block title %}Catálogo de Libros - SDS Library{% endblock %}

{% block content %}
<div class="container">
  <h2 class="mb-4" style="font-family: 'Merriweather', serif;">Catálogo de Libros</h2>

  <div class="row">
    {% if libros.items %}
      {% for libro in libros.items %}
        <div class="col-md-4 col-lg-3 mb-4">
          <div class="card h-100 shadow-sm border-0 position-relative">

            <!-- Portada -->
            <img src="{{ libro.portada_url if libro.portada_url else url_for('static', filename='imagenes/portada_default.png') }}"
                 class="card-img-top"
                 alt="Portada del libro '{{ libro.titulo }}'"
                 style="height: 280px; object-fit: contain; padding: 10px; background-color: #1e293b; border-radius: 8px;">

            <div class="card-body d-flex flex-column">
              <h5 class="card-title text-white">{{ libro.titulo }}</h5>
              <p class="card-text mb-1">Autor: {{ libro.autor }}</p>
              <p class="card-text">
                <small class="text-info">
                  {% if libro.cantidad_disponible > 0 %}
                    Disponible: {{ libro.cantidad_disponible }}
                  {% else %}
                    No disponible
                  {% endif %}
                </small>
              </p>

              <div class="mt-auto">
                {% if current_user.is_authenticated and current_user.rol == 'lector' %}
                  <!-- Siempre permite reservar -->
                  <a href="{{ url_for('main.reservar_libro_lector', libro_id=libro.id) }}"
                     class="btn btn-success btn-sm w-100 mb-2">
                    <i class="bi bi-bookmark-check-fill me-1"></i> Reservar
                  </a>
                {% endif %}

                <!-- Ver Detalles -->
                <a href="{{ url_for('main.detalle_libro', libro_id=libro.id) }}"
                   class="btn btn-outline-primary btn-sm w-100">
                  <i class="bi bi-eye me-1"></i> Ver Detalles
                </a>
              </div>
            </div>
          </div>
        </div>
      {% endfor %}
    {% else %}
      <p class="text-muted">No hay libros disponibles.</p>
    {% endif %}
  </div>

  <nav aria-label="Paginación de libros" class="mt-4">
    <ul class="pagination justify-content-center">
      {% if libros.has_prev %}
        <li class="page-item">
          <a class="page-link" href="{{ url_for('main.catalogo', page=libros.prev_num) }}">Anterior</a>
        </li>
      {% else %}
        <li class="page-item disabled"><span class="page-link">Anterior</span></li>
      {% endif %}

      {% for page_num in libros.iter_pages() %}
        {% if page_num %}
          {% if page_num == libros.page %}
            <li class="page-item active"><span class="page-link">{{ page_num }}</span></li>
          {% else %}
            <li class="page-item">
              <a class="page-link" href="{{ url_for('main.catalogo', page=page_num) }}">{{ page_num }}</a>
            </li>
          {% endif %}
        {% else %}
          <li class="page-item disabled"><span class="page-link">…</span></li>
        {% endif %}
      {% endfor %}

      {% if libros.has_next %}
        <li class="page-item">
          <a class="page-link" href="{{ url_for('main.catalogo', page=libros.next_num) }}">Siguiente</a>
        </li>
      {% else %}
        <li class="page-item disabled"><span class="page-link">Siguiente</span></li>
      {% endif %}
    </ul>
  </nav>
</div>
{% endblock %}


reservas

{% extends "base.html" %}

{% block title %}Reservar Libro{% endblock %}

{% block content %}
<div class="container mt-5">
  <div class="row justify-content-center">
    <div class="col-md-8">

      <h2 class="mb-4 text-center">Reservar: <span class="text-primary">{{ libro.titulo }}</span></h2>

      <div class="card mb-4 shadow-sm border-0 overflow-hidden">
        <div class="row g-0">
          <div class="col-md-4">
            <img src="{{ libro.portada_url if libro.portada_url else url_for('static', filename='imagenes/portada_default.png') }}"
                 alt="Portada de {{ libro.titulo }}"
                 class="img-fluid h-100"
                 style="object-fit: cover; min-height: 220px;">
          </div>
          <div class="col-md-8 d-flex align-items-center">
            <div class="card-body p-3">
              <h5 class="card-title mb-2">{{ libro.titulo }}</h5>
              <p class="mb-1"><strong>Autor:</strong> {{ libro.autor }}</p>
              <p class="mb-1"><strong>Categoría:</strong> {{ libro.categoria or 'N/A' }}</p>
              <p class="mb-1"><strong>Editorial:</strong> {{ libro.editorial or 'N/A' }}</p>
              <p class="mb-0"><strong>Disponible:</strong>
                {% if libro.cantidad_disponible > 0 %}
                  <span class="badge bg-success">{{ libro.cantidad_disponible }}</span>
                {% else %}
                  <span class="badge bg-danger">No disponible</span>
                {% endif %}
              </p>
            </div>
          </div>
        </div>
      </div>

      <!-- Siempre muestra el formulario -->
      <form method="POST" class="card p-4 shadow-sm border-0">
        {{ form.hidden_tag() }}

        <div class="mb-3">
          <label for="llave_prestamo" class="form-label">Llave de Préstamo</label>
          {{ form.llave_prestamo(class="form-control", placeholder="Ejemplo: 123-456") }}
          {% for error in form.llave_prestamo.errors %}
            <div class="text-danger">{{ error }}</div>
          {% endfor %}
        </div>

        <div class="d-grid gap-2">
          <button type="submit" class="btn btn-success">
            <i class="bi bi-bookmark-check-fill me-1"></i> Confirmar Reserva
          </button>
          <a href="{{ url_for('main.catalogo') }}" class="btn btn-secondary">
            <i class="bi bi-x-circle me-1"></i> Cancelar
          </a>
        </div>
      </form>

    </div>
  </div>
</div>
{% endblock %}


ruta

# Reservar libro como lector
@main.route('/reservar/<int:libro_id>', methods=['GET', 'POST'])
@login_required
@roles_requeridos('lector')
@nocache
def reservar_libro_lector(libro_id):
    libro = Libro.query.get_or_404(libro_id)
    form = ReservaLectorForm()

    if form.validate_on_submit():
        if current_user.llave_prestamo != form.llave_prestamo.data:
            flash('Llave incorrecta.', 'danger')
            return redirect(url_for('main.reservar_libro_lector', libro_id=libro.id))

        # Verifica si ya tiene una reserva activa o pendiente
        reserva_existente = Reserva.query.filter_by(
            libro_id=libro.id,
            usuario_id=current_user.id
        ).filter(Reserva.estado.in_(['pendiente', 'activa'])).first()

        if reserva_existente:
            flash('Ya tienes una reserva para este libro.', 'warning')
            return redirect(url_for('main.catalogo'))

        # ✅ Si hay stock → reserva activa y descuenta 1
        if libro.cantidad_disponible > 0:
            nueva_reserva = Reserva(
                usuario_id=current_user.id,
                libro_id=libro.id,
                estado='activa'
            )
            libro.cantidad_disponible -= 1
            libro.actualizar_estado()
            mensaje_estado = '✅ Reserva ACTIVADA. Pasa a recoger tu libro.'
        else:
            # ✅ Sin stock → reserva pendiente en cola
            posicion = Reserva.query.filter_by(libro_id=libro.id, estado='pendiente').count() + 1
            nueva_reserva = Reserva(
                usuario_id=current_user.id,
                libro_id=libro.id,
                posicion=posicion,
                estado='pendiente'
            )
            mensaje_estado = f'⏳ Reserva PENDIENTE. Lugar: {posicion}.'

        try:
            db.session.add(nueva_reserva)
            db.session.commit()

            # Envía correo de confirmación
            msg = Message(
                'Reserva registrada - Biblioteca',
                sender='noreply@biblioteca.com',
                recipients=[current_user.correo]
            )
            msg.body = f'''
Hola {current_user.nombre},

Tu reserva para "{libro.titulo}" ha sido registrada.
Estado: {nueva_reserva.estado.capitalize()}
{'Lugar en la cola: ' + str(posicion) if nueva_reserva.estado == 'pendiente' else ''}

Te notificaremos cualquier cambio.
'''
            mail.send(msg)

            logging.info(f"Reserva creada: Libro {libro.id}, Usuario {current_user.id}, Estado {nueva_reserva.estado}")
            flash(mensaje_estado, 'success')

        except Exception as e:
            db.session.rollback()
            logging.error(f"Error creando reserva libro {libro.id}: {e}")
            flash('Error al registrar la reserva.', 'danger')

        return redirect(url_for('main.catalogo'))

    return render_template('reservar_libro.html', libro=libro, form=form)
