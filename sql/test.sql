-- Criando tabelas baseadas no meu programa de monitoramento de reservatórios
CREATE TABLE users (
    id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,  
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    email_verified_at TIMESTAMP NULL DEFAULT NULL,
    password VARCHAR(255) NOT NULL,
    remember_token VARCHAR(100) NULL,
    is_admin BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP NULL DEFAULT NULL,
    updated_at TIMESTAMP NULL DEFAULT NULL
);

CREATE TABLE password_reset_tokens (
    email VARCHAR(255) PRIMARY KEY,
    token VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NULL DEFAULT NULL
);

CREATE TABLE sessions (
    id VARCHAR(255) PRIMARY KEY,
    user_id BIGINT NULL,
    ip_address VARCHAR(45) NULL,
    user_agent TEXT NULL,
    payload TEXT NOT NULL,  -- Use TEXT em vez de LONGTEXT
    last_activity INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
);

CREATE TABLE reservatorios (
    id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,  -- Auto incremento no PostgreSQL
    nome VARCHAR(255) NOT NULL,
    volume_maximo DECIMAL(15, 2) NOT NULL,
    volume_atual DECIMAL(15, 2) NOT NULL,
    ultima_atualizacao TIMESTAMP NOT NULL,
    descricao TEXT NULL,
    user_id BIGINT NOT NULL,
    created_at TIMESTAMP NULL DEFAULT NULL,
    updated_at TIMESTAMP NULL DEFAULT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE INDEX idx_reservatorios_created_at ON reservatorios(created_at);
CREATE INDEX idx_reservatorios_updated_at ON reservatorios(updated_at);
