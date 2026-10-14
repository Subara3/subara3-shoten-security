<?php require 'auth.php';
$res = mysqli_query(db(), 'SELECT * FROM orders ORDER BY ordered_at DESC LIMIT 50');
?><!doctype html><meta charset="utf-8"><title>注文一覧</title>
<h1>注文一覧</h1><p><a href="members.php">会員一覧</a> / <a href="export.php">会員CSV出力</a> / <a href="admins.php">管理者</a></p>
<table border="1"><tr><th>注文</th><th>お届け先</th><th>金額</th><th>日時</th></tr>
<?php while ($o = mysqli_fetch_assoc($res)): ?>
<tr><td><?= (int)$o['id'] ?></td><td><?= h($o['ship_name']) ?></td><td><?= number_format($o['total']) ?></td><td><?= h($o['ordered_at']) ?></td></tr>
<?php endwhile; ?></table>
