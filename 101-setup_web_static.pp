# Ensure the package 'nginx' is installed
package { 'nginx':
  ensure => installed,
}

# Ensure nginx service is running and enabled at boot
service { 'nginx':
  ensure     => running,
  enable     => true,
  subscribe  => Package['nginx'],
}

# Ensure /data directory exists
file { '/data':
  ensure => directory,
  owner  => 'root',
  group  => 'root',
  mode   => '0755',
}

# Ensure /data/web_static directory exists
file { '/data/web_static':
  ensure => directory,
  owner  => 'root',
  group  => 'root',
  mode   => '0755',
}

# Ensure /data/web_static/releases directory exists
file { '/data/web_static/releases':
  ensure => directory,
  owner  => 'root',
  group  => 'root',
  mode   => '0755',
}

# Ensure /data/web_static/shared directory exists
file { '/data/web_static/shared':
  ensure => directory,
  owner  => 'root',
  group  => 'root',
  mode   => '0755',
}

# Ensure /data/web_static/releases/test directory exists
file { '/data/web_static/releases/test':
  ensure => directory,
  owner  => 'root',
  group  => 'root',
  mode   => '0755',
}

# Create a simple HTML file
file { '/data/web_static/releases/test/index.html':
  ensure  => file,
  content => '<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>',
  owner   => 'root',
  group   => 'root',
  mode    => '0644',
}

# Ensure the /data/web_static/current symbolic link exists and points to the /data/web_static/releases/test directory
file { '/data/web_static/current':
  ensure => link,
  target => '/data/web_static/releases/test',
}

# Ensure the Nginx configuration for hbnb_static
file { '/etc/nginx/sites-available/default':
  ensure  => file,
  content => '
server {
    listen 80 default_server;
    listen [::]:80 default_server;

    root /var/www/html;
    index index.html index.htm index.nginx-debian.html;

    server_name _;

    location / {
        try_files $uri $uri/ =404;
    }

    location /hbnb_static {
        alias /data/web_static/current;
        index index.html index.htm;
    }
}',
  notify  => Service['nginx'],
}

# Ensure the Nginx service is restarted if the configuration changes
service { 'nginx':
  ensure    => running,
  enable    => true,
  subscribe => File['/etc/nginx/sites-available/default'],
}
