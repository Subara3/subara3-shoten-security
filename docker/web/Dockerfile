# 2019年に組んだまま更新していない想定（PHP 7.4 は 2022-11 にサポート終了）
FROM php:7.4-apache
RUN docker-php-ext-install mysqli \
 # 当時のレンタルサーバの既定に合わせて、ディレクトリ一覧を出す設定にしておく
 && sed -i 's/Options -Indexes/Options +Indexes/' /etc/apache2/conf-enabled/docker-php.conf
