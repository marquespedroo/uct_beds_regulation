{% extends 'base.html' %}

{% block body %}

<body>

  <!-- ======= Header ======= -->
  <header id="header" class="header fixed-top d-flex align-items-center">
    <div class="d-flex align-items-center justify-content-between">
      <a href="index.html" class="logo d-flex align-items-center" style="text-decoration: none;">
        <img src="static/assets/img/logo.png" alt="">
        <span class="d-none d-lg-block">CRDF</span>
      </a>
    </div>
    <nav class="header-nav ms-auto d-flex justify-content-end">
      {% if current_user.is_authenticated %}
      <ul class="d-flex align-items-center">
        <li class="nav-item">
          <a class="nav-link fw-bold" href="{{ url_for('logout') }}" style="padding-right: 35px;">Sair</a>
        </li>
      </ul>
      {% endif %}
    </nav>
  </header><!-- End Header -->
  <style>
    body {
      font-family: 'Open Sans', sans-serif;
    }
    th,
    td {
      text-align: center;
    }
    h1,
    h2 {
      font-weight: bold;
    }
  </style>

  <main class="container">
    <br><br><br><br><br>

    <section class="section">
      <div class="row">
        <div class="col-lg-8">

          <div class="card">
            <div class="card-body text-center">
              <h5  class="card-title"><h4>{{ hospital }}</h4></h5>

            </div>
          </div>

        </div>
    <div class="col-lg-8">

      <section class="section">

        <div class="card">
          <div class="card-body text-center" class="card-body">
            <br><br>
          {% for tipo_leito, leitos in bed.items() %}
          <h4>Tipo de Leito: <strong>{{ tipo_leito }}</strong></h4>
          <table class="table table-striped">
            <thead>
              <tr>
                <th scope="col">Número do leito</th>
                <th scope="col">Status</th>
                <th scope="col">Atualizar</th>
              </tr>
            </thead>
            <tbody>
              {% for numero_leito in range(1, leitos + 1) %}
              <tr>
                <td>{{ numero_leito }}</td>
                <td><!-- Status do leito --></td>
                <td><a href="{{ url_for('atualizar_leito', hospital=hospital, tipo_leito=tipo_leito, numero_leito=numero_leito) }}" class="btn btn-info rounded-pill">Atualizar Leito</a></td>
              </tr>
              {% endfor %}
            </tbody>
          </table>
          {% endfor %}
          </div>
        </div>
        <!-- End Table with stripped rows -->

      </section>

      {% with messages = get_flashed_messages(with_categories=True) %}
      {% if messages %}
      {% for category, message in messages %}
      <div class="alert alert-{{ category }}">
        {{ message }}
      </div>
      {% endfor %}
      {% endif %}
      {% endwith %}

    </div>

  </main><!-- End #main -->

  <!-- ======= Footer ======= -->
  <footer id="footer" class="footer" style="display: inline;">
    <div class="copyright">
      &copy; Copyright <strong><span>NiceAdmin</span></strong>. All Rights Reserved
    </div>
    <div class="credits">
      <!-- All the links in the footer should remain intact. -->
      <!-- You can delete the links only if you purchased the pro version. -->
      <!-- Licensing information: https://bootstrapmade.com/license/ -->
      <!-- Purchase the pro version with working PHP/AJAX contact form: https://bootstrapmade.com/nice-admin-bootstrap-admin-html-template/ -->
      Designed by <a href="https://bootstrapmade.com/">BootstrapMade</a>
    </div>
  </footer><!-- End Footer -->

  <a href="#" class="back-to-top d-flex align-items-center justify-content-center"><i class="bi bi-arrow-up-short"></i></a>

</body>
{% endblock %}
</html>