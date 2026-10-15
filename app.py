<!DOCTYPE html>
<html lang="nl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>KM-registratie</title>
    <style>
        body { font-family: Arial; margin: 0; padding: 20px; background: #CFA94A; }
        h2 { text-align: center; margin-bottom: 20px; }
        form { background: white; padding: 20px; border-radius: 12px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
        label { font-size: 16px; margin-top: 15px; display: block; }
        input { width: 100%; padding: 14px; font-size: 18px; border: 1px solid #ccc; border-radius: 8px; margin-top: 6px; }
        .btn-row { display: flex; gap: 10px; margin-top: 10px; }
        .quick-btn { flex: 1; padding: 12px; background: #333; color: white; border: none; border-radius: 8px; font-size: 14px; }
        button[type="submit"] { width: 100%; padding: 16px; margin-top: 25px; background: #333; color: white; font-size: 18px; border: none; border-radius: 8px; }
    </style>
</head>
<body>

<h2>KM-registratie</h2>

<form id="kmForm">
    <label>Datum</label>
    <input type="date" id="datum" name="datum" required>

    <label>Beginstand (km)</label>
    <input type="number" id="begin" name="begin" required>

    <label>Eindstand (km)</label>