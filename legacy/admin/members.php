<?php require 'auth.php';
$res = mysqli_query(db(), 'SELECT * FROM members ORDER BY id DESC LIMIT 100');
?><!doctype html><meta charset="utf-8"><title>会員一覧</title><h1>会員一覧</h1>
<table border="1"><?php while ($m = mysqli_fetch_assoc($res)): ?>
<tr><td><?= (int)$m['id'] ?></td><td><?= h($m['name']) ?></td><td><?= h($m['email']) ?></td><td><?= h($m['status']) ?></td></tr>
<?php endwhile; ?></table>
