<!DOCTYPE html>
<html>
	<head>
		<title>1.0.1</title>
		<script src="https://code.angularjs.org/1.0.1/angular-1.0.1.min.js"></script>
	</head>
	<body ng-app="">
		<a href="?vulnerable=payload">Payload</a>
		<?php if(isset($_GET['vulnerable'])): ?>
		<?= //htmlentities($_GET['vulnerable']); ?>
		<?php endif; ?>
	</body>
</html>