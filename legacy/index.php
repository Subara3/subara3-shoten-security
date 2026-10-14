<?php require 'config.php';
$res = mysqli_query(db(), 'SELECT * FROM products ORDER BY id');
?><!doctype html><meta charset="utf-8"><title><?= SHOP_NAME ?></title>
<h1><?= SHOP_NAME ?></h1>
<p>和雑貨の通信販売。<a href="login.php">会員ログイン</a></p>
<ul>
<?php while ($p = mysqli_fetch_assoc($res)): ?>
<li><?= h($p['name']) ?> … <?= number_format($p['price']) ?>円</li>
<?php endwhile; ?>
</ul>
