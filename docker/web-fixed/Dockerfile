# 点検後：PHP 8.3 に上げる。ディレクトリ一覧は出さない（イメージの既定のまま）
FROM php:8.3-apache
RUN docker-php-ext-install mysqli \
 && a2enmod headers
