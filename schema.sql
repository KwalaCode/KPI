DROP TABLE IF EXISTS kpi;

CREATE TABLE kpi (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    temps_livraison REAL NOT NULL,
    taux_service REAL NOT NULL,
    niveau_stock REAL NOT NULL
);

