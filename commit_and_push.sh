#!/bin/bash

# Script para fazer commit e push das melhorias para o GitHub
# Uso: ./commit_and_push.sh "mensagem do commit"

# Verifica se foi fornecida uma mensagem de commit
if [ -z "$1" ]; then
    echo "❌ Erro: Por favor, forneça uma mensagem de commit"
    echo "Uso: ./commit_and_push.sh \"mensagem do commit\""
    exit 1
fi

COMMIT_MESSAGE="$1"

echo "🚀 Iniciando processo de commit e push..."
echo "📝 Mensagem do commit: $COMMIT_MESSAGE"
echo ""

# Adiciona todos os arquivos modificados
echo "📦 Adicionando arquivos..."
git add .

# Verifica se há mudanças para commit
if git diff --cached --quiet; then
    echo "✅ Nenhuma mudança para commit"
    exit 0
fi

# Mostra os arquivos que serão commitados
echo ""
echo "📋 Arquivos que serão commitados:"
git diff --cached --name-only
echo ""

# Faz o commit
echo "💾 Fazendo commit..."
git commit -m "$COMMIT_MESSAGE"

if [ $? -ne 0 ]; then
    echo "❌ Erro ao fazer commit"
    exit 1
fi

echo "✅ Commit realizado com sucesso!"
echo ""

# Mostra o status do repositório
echo "📊 Status do repositório:"
git status
echo ""

# Pergunta se deseja fazer push
read -p "Deseja fazer push para o GitHub? (s/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Ss]$ ]]; then
    echo "📤 Fazendo push para o GitHub..."
    git push origin main

    if [ $? -ne 0 ]; then
        echo "❌ Erro ao fazer push"
        exit 1
    fi

    echo "✅ Push realizado com sucesso!"
    echo ""
    echo "🎉 Melhorias enviadas para o GitHub!"
    echo "🔗 Repositório: https://github.com/Ronbragaglia/Assistente_simples"
else
    echo "ℹ️  Push não realizado. Você pode fazer manualmente com:"
    echo "   git push origin main"
fi
