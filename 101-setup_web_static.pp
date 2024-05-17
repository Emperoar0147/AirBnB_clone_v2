# 101-setup_web_static.pp

# Ensure nginx is installed
package { 'nginx':
  ensure => installed,
}

# Ensure nginx service is running and enabled
service { 'nginx':
  ensure     => running,
  enable     => true,
  subscribe  => File['/etc/nginx/sites-available/default'],
}

# Create the directory structure
file { '/data/web_static/releases/test/':
  ensure => directory,
  owner  => 'www-data',
  group  => 'www-data',
  mode   => '0755',
  require => Exec['mkdir -p /data/web_static/releases/test/'],
}

file { '/data/web_static/shared/':
  ensure => directory,
  owner  => 'www-data',
  group  => 'www-data',
  mode   => '0755',
}

exec { 'mkdir -p /data/web_static/releases/test/':
  command => 'mkdir -p /data/web_static/releases/test/',
  creates => '/data/web_static/releases/test/',
}

exec { 'mkdir -p /data/web_static/shared/':
  command => 'mkdir -p /data/web_static/shared/',
  creates => '/data/web_static/shared/',
}

# Create a test index.html file
file { '/data/web_static/releases/test/index.html':
  ensure  => file,
  content => '<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>',
  owner  => 'www-data',
  group  => 'www-data',
  mode   => '0644',
}

# Create the symbolic link
file { '/data/web_static/current':
  ensure => link,
  target => '/data/web_static/releases/test',
  owner  => 'www-data',
  group  => 'www-data',
  require => File['/data/web_static/releases/test/'],
}

# Update nginx configuration
file { '/etc/nginx/sites-available/default':
  ensure  => file,
  content => template('nginx/default.erb'),
  notify  => Service['nginx'],
}

# Template for Nginx configuration
file { 'nginx_default_template':
  ensure  => file,
  path    => '/etc/puppetlabs/code/environments/production/modules/nginx/templates/default.erb',
  content => '
server {
    listen 80 default_server;
    listen [::]:80 default_server;
    
    root /var/www/html;
    index index.html index.htm index.nginx-debian.html;
    
    server_name _;

    location /hbnb_static/ {
        alias /data/web_static/current/;
        index index.html index.htm;
    }

    location / {
        try_files $uri $uri/ =404;
    }
}
',
}
