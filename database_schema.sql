-- Finanzverwaltungstool Database Schema
-- MariaDB Schema für das Finanzverwaltungssystem

CREATE DATABASE IF NOT EXISTS finaz_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE finaz_db;

-- Tabelle für Konten
CREATE TABLE IF NOT EXISTS accounts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    account_type ENUM('Girokonto', 'Sparkonto', 'Kreditkarte', 'Bargeld', 'Sonstiges') NOT NULL,
    balance DECIMAL(15, 2) DEFAULT 0.00,
    currency VARCHAR(3) DEFAULT 'EUR',
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY unique_account_name (name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabelle für Kategorien
CREATE TABLE IF NOT EXISTS categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    category_type ENUM('Einnahme', 'Ausgabe') NOT NULL,
    description TEXT,
    parent_id INT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY unique_category (name, category_type),
    FOREIGN KEY (parent_id) REFERENCES categories(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabelle für Transaktionen
CREATE TABLE IF NOT EXISTS transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    account_id INT NOT NULL,
    category_id INT NOT NULL,
    transaction_type ENUM('Einnahme', 'Ausgabe', 'Transfer') NOT NULL,
    amount DECIMAL(15, 2) NOT NULL,
    description TEXT,
    transaction_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (account_id) REFERENCES accounts(id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE RESTRICT,
    INDEX idx_transaction_date (transaction_date),
    INDEX idx_account_id (account_id),
    INDEX idx_category_id (category_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabelle für Budgets
CREATE TABLE IF NOT EXISTS budgets (
    id INT AUTO_INCREMENT PRIMARY KEY,
    category_id INT NOT NULL,
    amount DECIMAL(15, 2) NOT NULL,
    period_start DATE NOT NULL,
    period_end DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE,
    INDEX idx_period (period_start, period_end)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Erstelle Standard-Kategorien
INSERT INTO categories (name, category_type, description) VALUES
    ('Gehalt', 'Einnahme', 'Monatliches Gehalt'),
    ('Bonus', 'Einnahme', 'Bonuszahlungen'),
    ('Investitionen', 'Einnahme', 'Kapitalerträge'),
    ('Lebensmittel', 'Ausgabe', 'Einkäufe für Lebensmittel'),
    ('Miete', 'Ausgabe', 'Wohnungsmiete'),
    ('Transport', 'Ausgabe', 'Fahrtkosten und ÖPNV'),
    ('Unterhaltung', 'Ausgabe', 'Freizeit und Entertainment'),
    ('Gesundheit', 'Ausgabe', 'Medizinische Ausgaben'),
    ('Versicherungen', 'Ausgabe', 'Versicherungsbeiträge'),
    ('Sonstiges', 'Ausgabe', 'Verschiedene Ausgaben');
