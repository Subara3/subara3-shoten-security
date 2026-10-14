<?php require 'auth.php';
$res = mysqli_query(db(), 'SELECT login, role, active, note, created_at, last_login FROM admins');
?><!doctype html><meta charset="utf-8"><title>管理者</title><h1>管理者アカウント</h1>
<table border="1"><?php while ($a = mysqli_fetch_assoc($res)): ?>
<tr><?php foreach ($a as $v): ?><td><?= h($v) ?></td><?php endforeach; ?></tr>
<?php endwhile; ?></table>
