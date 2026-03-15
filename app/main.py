import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from conexao_bd import ConexaoBD
from gerenciador_crud import GerenciadorProdutos, GerenciadorClientes, GerenciadorVendas
from modelos import Produto, Cliente, Venda

st.set_page_config(
    page_title="Sistema de Supermercado",
    page_icon="🛒",
    layout="wide"
)

if 'conexao' not in st.session_state:
    st.session_state.conexao = ConexaoBD()
    st.session_state.gerenciador_produtos = GerenciadorProdutos(st.session_state.conexao)
    st.session_state.gerenciador_clientes = GerenciadorClientes(st.session_state.conexao)
    st.session_state.gerenciador_vendas = GerenciadorVendas(st.session_state.conexao)

def pagina_produtos():
    st.header("📦 Gerenciamento de Produtos")
    
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "Listar Todos", "Inserir", "Alterar", "Pesquisar", "Remover", "Exibir Um"
    ])
    
    with tab1:
        st.subheader("Lista de Produtos")
        produtos = st.session_state.gerenciador_produtos.listar_todos()
        
        if produtos:
            dados = []
            for p in produtos:
                dados.append({
                    'Código': p.codigo,
                    'Nome': p.nome,
                    'Preço': f"R$ {p.preco:.2f}",
                    'Estoque': p.quantidade_estoque,
                    'Categoria': p.categoria,
                    'Fornecedor': p.fornecedor,
                    'Valor Total': f"R$ {p.calcular_valor_total_estoque():.2f}"
                })
            
            df = pd.DataFrame(dados)
            st.dataframe(df, use_container_width=True)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total de Produtos", len(produtos))
            with col2:
                valor_total = sum(p.calcular_valor_total_estoque() for p in produtos)
                st.metric("Valor Total em Estoque", f"R$ {valor_total:.2f}")
            with col3:
                produtos_baixo = st.session_state.gerenciador_produtos.obter_produtos_em_falta()
                st.metric("Produtos com Estoque Baixo", len(produtos_baixo))
        else:
            st.info("Nenhum produto cadastrado")
    
    with tab2:
        st.subheader("Inserir Novo Produto")
        
        with st.form("form_inserir_produto"):
            nome = st.text_input("Nome do Produto")
            preco = st.number_input("Preço", min_value=0.0, step=0.01, format="%.2f")
            quantidade = st.number_input("Quantidade em Estoque", min_value=0, step=1)
            categoria = st.selectbox("Categoria", 
                ["Alimentos", "Bebidas", "Limpeza", "Higiene", "Laticínios", "Outros"])
            fornecedor = st.text_input("Fornecedor")
            
            if st.form_submit_button("Inserir Produto"):
                if nome and preco > 0 and fornecedor:
                    produto = Produto(
                        nome=nome,
                        preco=preco,
                        quantidade_estoque=quantidade,
                        categoria=categoria,
                        fornecedor=fornecedor
                    )
                    
                    codigo = st.session_state.gerenciador_produtos.inserir(produto)
                    if codigo:
                        st.success(f"Produto inserido com sucesso! Código: {codigo}")
                    else:
                        st.error("Erro ao inserir produto")
                else:
                    st.error("Preencha todos os campos obrigatórios")
    
    with tab3:
        st.subheader("Alterar Produto")
        
        produtos = st.session_state.gerenciador_produtos.listar_todos()
        if produtos:
            produto_selecionado = st.selectbox(
                "Selecione o Produto",
                options=produtos,
                format_func=lambda p: f"{p.codigo} - {p.nome}",
                key="alterar_produto_select"
            )
            
            if produto_selecionado:
                with st.form("form_alterar_produto"):
                    nome = st.text_input("Nome", value=produto_selecionado.nome)
                    preco = st.number_input("Preço", value=float(produto_selecionado.preco), 
                                           min_value=0.0, step=0.01, format="%.2f")
                    quantidade = st.number_input("Quantidade", 
                                                value=produto_selecionado.quantidade_estoque,
                                                min_value=0, step=1)
                    categoria = st.selectbox("Categoria", 
                        ["Alimentos", "Bebidas", "Limpeza", "Higiene", "Laticínios", "Outros"],
                        index=["Alimentos", "Bebidas", "Limpeza", "Higiene", "Laticínios", "Outros"]
                              .index(produto_selecionado.categoria))
                    fornecedor = st.text_input("Fornecedor", value=produto_selecionado.fornecedor)
                    
                    if st.form_submit_button("Alterar Produto"):
                        produto_selecionado.nome = nome
                        produto_selecionado.preco = preco
                        produto_selecionado.quantidade_estoque = quantidade
                        produto_selecionado.categoria = categoria
                        produto_selecionado.fornecedor = fornecedor
                        
                        if st.session_state.gerenciador_produtos.alterar(produto_selecionado):
                            st.success("Produto alterado com sucesso!")
                        else:
                            st.error("Erro ao alterar produto")
        else:
            st.info("Nenhum produto cadastrado")
    
    with tab4:
        st.subheader("Pesquisar Produto por Nome")
        
        termo_busca = st.text_input("Digite o nome ou parte do nome do produto")
        
        if st.button("Pesquisar"):
            if termo_busca:
                produtos = st.session_state.gerenciador_produtos.pesquisar_por_nome(termo_busca)
                
                if produtos:
                    dados = []
                    for p in produtos:
                        dados.append({
                            'Código': p.codigo,
                            'Nome': p.nome,
                            'Preço': f"R$ {p.preco:.2f}",
                            'Estoque': p.quantidade_estoque,
                            'Categoria': p.categoria,
                            'Fornecedor': p.fornecedor
                        })
                    
                    df = pd.DataFrame(dados)
                    st.dataframe(df, use_container_width=True)
                else:
                    st.info("Nenhum produto encontrado")
            else:
                st.warning("Digite um termo para pesquisar")
    
    with tab5:
        st.subheader("Remover Produto")
        
        produtos = st.session_state.gerenciador_produtos.listar_todos()
        if produtos:
            produto_remover = st.selectbox(
                "Selecione o Produto para Remover",
                options=produtos,
                format_func=lambda p: f"{p.codigo} - {p.nome}",
                key="remover_produto_select"
            )
            
            if produto_remover:
                st.warning(f"Você está prestes a remover: {produto_remover.nome}")
                
                if st.button("Confirmar Remoção", type="primary"):
                    if st.session_state.gerenciador_produtos.remover(produto_remover.codigo):
                        st.success("Produto removido com sucesso!")
                        st.rerun()
                    else:
                        st.error("Erro ao remover produto")
        else:
            st.info("Nenhum produto cadastrado")
    
    with tab6:
        st.subheader("Exibir Detalhes de Um Produto")
        
        produtos = st.session_state.gerenciador_produtos.listar_todos()
        if produtos:
            produto_exibir = st.selectbox(
                "Selecione o Produto",
                options=produtos,
                format_func=lambda p: f"{p.codigo} - {p.nome}",
                key="exibir_produto_select"
            )
            
            if st.button("Exibir Detalhes"):
                produto = st.session_state.gerenciador_produtos.exibir_um(produto_exibir.codigo)
                
                if produto:
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**Código:** {produto.codigo}")
                        st.write(f"**Nome:** {produto.nome}")
                        st.write(f"**Categoria:** {produto.categoria}")
                    
                    with col2:
                        st.write(f"**Preço:** {produto.formatar_preco()}")
                        st.write(f"**Estoque:** {produto.quantidade_estoque} unidades")
                        st.write(f"**Fornecedor:** {produto.fornecedor}")
                    
                    st.write(f"**Valor Total em Estoque:** R$ {produto.calcular_valor_total_estoque():.2f}")
                else:
                    st.error("Produto não encontrado")
        else:
            st.info("Nenhum produto cadastrado")


def pagina_clientes():
    st.header("👥 Gerenciamento de Clientes")
    
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "Listar Todos", "Inserir", "Alterar", "Pesquisar", "Remover", "Exibir Um"
    ])
    
    with tab1:
        st.subheader("Lista de Clientes")
        clientes = st.session_state.gerenciador_clientes.listar_todos()
        
        if clientes:
            dados = []
            for c in clientes:
                dados.append({
                    'Código': c.codigo,
                    'Nome': c.nome,
                    'CPF': c.formatar_cpf(),
                    'Email': c.email,
                    'Telefone': c.formatar_telefone(),
                    'Endereço': c.endereco
                })
            
            df = pd.DataFrame(dados)
            st.dataframe(df, use_container_width=True)
            
            st.metric("Total de Clientes", len(clientes))
        else:
            st.info("Nenhum cliente cadastrado")
    
    with tab2:
        st.subheader("Inserir Novo Cliente")
        
        with st.form("form_inserir_cliente"):
            nome = st.text_input("Nome Completo")
            cpf = st.text_input("CPF (apenas números)")
            email = st.text_input("Email")
            telefone = st.text_input("Telefone (apenas números)")
            endereco = st.text_area("Endereço")
            
            if st.form_submit_button("Inserir Cliente"):
                if nome and cpf:
                    if st.session_state.gerenciador_clientes.verificar_cpf_existe(cpf):
                        st.error("CPF já cadastrado!")
                    else:
                        cliente = Cliente(
                            nome=nome,
                            cpf=cpf,
                            email=email,
                            telefone=telefone,
                            endereco=endereco
                        )
                        
                        if cliente.validar_cpf():
                            codigo = st.session_state.gerenciador_clientes.inserir(cliente)
                            if codigo:
                                st.success(f"Cliente inserido com sucesso! Código: {codigo}")
                            else:
                                st.error("Erro ao inserir cliente")
                        else:
                            st.error("CPF inválido! Deve conter 11 dígitos")
                else:
                    st.error("Nome e CPF são obrigatórios")
    
    with tab3:
        st.subheader("Alterar Cliente")
        
        clientes = st.session_state.gerenciador_clientes.listar_todos()
        if clientes:
            cliente_selecionado = st.selectbox(
                "Selecione o Cliente",
                options=clientes,
                format_func=lambda c: f"{c.codigo} - {c.nome}",
                key="alterar_cliente_select"
            )
            
            if cliente_selecionado:
                with st.form("form_alterar_cliente"):
                    nome = st.text_input("Nome", value=cliente_selecionado.nome)
                    cpf = st.text_input("CPF", value=cliente_selecionado.cpf)
                    email = st.text_input("Email", value=cliente_selecionado.email)
                    telefone = st.text_input("Telefone", value=cliente_selecionado.telefone)
                    endereco = st.text_area("Endereço", value=cliente_selecionado.endereco)
                    
                    if st.form_submit_button("Alterar Cliente"):
                        if st.session_state.gerenciador_clientes.verificar_cpf_existe(
                            cpf, cliente_selecionado.codigo):
                            st.error("CPF já cadastrado para outro cliente!")
                        else:
                            cliente_selecionado.nome = nome
                            cliente_selecionado.cpf = cpf
                            cliente_selecionado.email = email
                            cliente_selecionado.telefone = telefone
                            cliente_selecionado.endereco = endereco
                            
                            if st.session_state.gerenciador_clientes.alterar(cliente_selecionado):
                                st.success("Cliente alterado com sucesso!")
                            else:
                                st.error("Erro ao alterar cliente")
        else:
            st.info("Nenhum cliente cadastrado")
    
    with tab4:
        st.subheader("Pesquisar Cliente por Nome")
        
        termo_busca = st.text_input("Digite o nome ou parte do nome do cliente")
        
        if st.button("Pesquisar"):
            if termo_busca:
                clientes = st.session_state.gerenciador_clientes.pesquisar_por_nome(termo_busca)
                
                if clientes:
                    dados = []
                    for c in clientes:
                        dados.append({
                            'Código': c.codigo,
                            'Nome': c.nome,
                            'CPF': c.formatar_cpf(),
                            'Email': c.email,
                            'Telefone': c.formatar_telefone()
                        })
                    
                    df = pd.DataFrame(dados)
                    st.dataframe(df, use_container_width=True)
                else:
                    st.info("Nenhum cliente encontrado")
            else:
                st.warning("Digite um termo para pesquisar")
    
    with tab5:
        st.subheader("Remover Cliente")
        
        clientes = st.session_state.gerenciador_clientes.listar_todos()
        if clientes:
            cliente_remover = st.selectbox(
                "Selecione o Cliente para Remover",
                options=clientes,
                format_func=lambda c: f"{c.codigo} - {c.nome}",
                key="remover_cliente_select"
            )
            
            if cliente_remover:
                st.warning(f"Você está prestes a remover: {cliente_remover.nome}")
                
                if st.button("Confirmar Remoção", type="primary"):
                    if st.session_state.gerenciador_clientes.remover(cliente_remover.codigo):
                        st.success("Cliente removido com sucesso!")
                        st.rerun()
                    else:
                        st.error("Erro ao remover cliente")
        else:
            st.info("Nenhum cliente cadastrado")
    
    with tab6:
        st.subheader("Exibir Detalhes de Um Cliente")
        
        clientes = st.session_state.gerenciador_clientes.listar_todos()
        if clientes:
            cliente_exibir = st.selectbox(
                "Selecione o Cliente",
                options=clientes,
                format_func=lambda c: f"{c.codigo} - {c.nome}",
                key="exibir_cliente_select"
            )
            
            if st.button("Exibir Detalhes"):
                cliente = st.session_state.gerenciador_clientes.exibir_um(cliente_exibir.codigo)
                
                if cliente:
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**Código:** {cliente.codigo}")
                        st.write(f"**Nome:** {cliente.nome}")
                        st.write(f"**CPF:** {cliente.formatar_cpf()}")
                    
                    with col2:
                        st.write(f"**Email:** {cliente.email}")
                        st.write(f"**Telefone:** {cliente.formatar_telefone()}")
                        st.write(f"**Endereço:** {cliente.endereco}")
                else:
                    st.error("Cliente não encontrado")
        else:
            st.info("Nenhum cliente cadastrado")


def pagina_vendas():
    st.header("💰 Realizar Vendas")
    
    tab1, tab2, tab3 = st.tabs(["Nova Venda", "Histórico de Vendas", "Cancelar Venda"])
    
    with tab1:
        st.subheader("Registrar Nova Venda")
        
        clientes = st.session_state.gerenciador_clientes.listar_todos()
        produtos = st.session_state.gerenciador_produtos.listar_todos()
        
        if not produtos:
            st.warning("Nenhum produto cadastrado. Cadastre produtos antes de realizar vendas.")
            return
        
        col1, col2 = st.columns(2)
        
        with col1:
            cliente_selecionado = st.selectbox(
                "Cliente (opcional)",
                options=[None] + clientes,
                format_func=lambda c: "Sem cliente" if c is None else f"{c.nome}",
                key="venda_cliente_select"
            )
        
        with col2:
            forma_pagamento = st.selectbox(
                "Forma de Pagamento",
                ["Dinheiro", "Cartão de Crédito", "Cartão de Débito", "PIX"],
                key="venda_forma_pagamento"
            )
        
        st.divider()
        st.subheader("Adicionar Produtos")
        
        if 'itens_venda' not in st.session_state:
            st.session_state.itens_venda = []
        
        col1, col2, col3 = st.columns([3, 1, 1])
        
        with col1:
            produto_add = st.selectbox(
                "Produto",
                options=produtos,
                format_func=lambda p: f"{p.nome} - R$ {p.preco:.2f} (Estoque: {p.quantidade_estoque})",
                key="venda_produto_add"
            )
        
        with col2:
            quantidade_add = st.number_input("Quantidade", min_value=1, value=1)
        
        with col3:
            if st.button("Adicionar", type="primary"):
                if produto_add.verificar_disponibilidade(quantidade_add):
                    st.session_state.itens_venda.append({
                        'produto': produto_add,
                        'quantidade': quantidade_add,
                        'subtotal': produto_add.preco * quantidade_add
                    })
                    st.success("Produto adicionado!")
                else:
                    st.error(f"Estoque insuficiente! Disponível: {produto_add.quantidade_estoque}")
        
        if st.session_state.itens_venda:
            st.divider()
            st.subheader("Itens da Venda")
            
            for i, item in enumerate(st.session_state.itens_venda):
                col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 1, 1])
                
                with col1:
                    st.write(item['produto'].nome)
                with col2:
                    st.write(f"Qtd: {item['quantidade']}")
                with col3:
                    st.write(f"R$ {item['produto'].preco:.2f}")
                with col4:
                    st.write(f"R$ {item['subtotal']:.2f}")
                with col5:
                    if st.button("Remover", key=f"remove_{i}"):
                        st.session_state.itens_venda.pop(i)
                        st.rerun()
            
            st.divider()
            
            total = sum(item['subtotal'] for item in st.session_state.itens_venda)
            
            col1, col2 = st.columns(2)
            with col1:
                desconto = st.number_input("Desconto (%)", min_value=0.0, max_value=100.0, value=0.0)
            
            total_com_desconto = total * (1 - desconto / 100)
            
            with col2:
                st.metric("Total da Venda", f"R$ {total_com_desconto:.2f}")
            
            if st.button("Finalizar Venda", type="primary", use_container_width=True):
                venda = Venda(cliente=cliente_selecionado)
                venda.desconto_total = desconto
                venda.forma_pagamento = forma_pagamento
                
                for item in st.session_state.itens_venda:
                    venda.adicionar_item(
                        item['produto'],
                        item['quantidade'],
                        item['produto'].preco
                    )
                
                venda.status = "concluida"
                codigo = st.session_state.gerenciador_vendas.inserir(venda)
                
                if codigo:
                    st.success(f"Venda realizada com sucesso! Código: {codigo}")
                    st.session_state.itens_venda = []
                    st.rerun()
                else:
                    st.error("Erro ao finalizar venda")
        else:
            st.info("Adicione produtos à venda")
    
    with tab2:
        st.subheader("Histórico de Vendas")
        
        vendas = st.session_state.gerenciador_vendas.listar_todos()
        
        if vendas:
            dados = []
            for v in vendas:
                dados.append({
                    'Código': v['codigo'],
                    'Cliente': v['nome_cliente'] or 'Não identificado',
                    'Data': v['data_venda'],
                    'Total': f"R$ {float(v['total'] or 0):.2f}",
                    'Pagamento': v['forma_pagamento'],
                    'Status': v['status']
                })
            
            df = pd.DataFrame(dados)
            st.dataframe(df, use_container_width=True)
            
            hoje = datetime.now()
            resumo_dia = st.session_state.gerenciador_vendas.obter_total_vendas_dia(hoje)
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Vendas Hoje", resumo_dia['quantidade_vendas'])
            with col2:
                st.metric("Faturamento Hoje", f"R$ {float(resumo_dia['total_vendido'] or 0):.2f}")
        else:
            st.info("Nenhuma venda realizada")
    
    with tab3:
        st.subheader("Cancelar Venda")
        
        vendas = st.session_state.gerenciador_vendas.listar_todos()
        vendas_ativas = [v for v in vendas if v['status'] != 'cancelada']
        
        if vendas_ativas:
            venda_cancelar = st.selectbox(
                "Selecione a Venda para Cancelar",
                options=vendas_ativas,
                format_func=lambda v: f"Código {v['codigo']} - {v['nome_cliente'] or 'Sem cliente'} - R$ {float(v['total'] or 0):.2f}",
                key="cancelar_venda_select"
            )
            
            if venda_cancelar:
                st.warning("O cancelamento irá devolver os produtos ao estoque")
                
                if st.button("Confirmar Cancelamento", type="primary"):
                    if st.session_state.gerenciador_vendas.cancelar_venda(venda_cancelar['codigo']):
                        st.success("Venda cancelada com sucesso!")
                        st.rerun()
                    else:
                        st.error("Erro ao cancelar venda")
        else:
            st.info("Nenhuma venda ativa para cancelar")


def pagina_relatorios():
    st.header("📊 Relatório Geral do Sistema")
    
    # --- RESUMO DE ESTOQUE ---
    st.subheader("📦 Posição do Estoque")
    produtos = st.session_state.gerenciador_produtos.listar_todos()
    
    total_produtos = len(produtos)
    valor_total_estoque = sum(p.calcular_valor_total_estoque() for p in produtos)
    produtos_em_falta = len(st.session_state.gerenciador_produtos.obter_produtos_em_falta())
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Itens Cadastrados", total_produtos)
    col2.metric("Valor Total do Estoque", f"R$ {valor_total_estoque:.2f}")
    col3.metric("Produtos em Falta", produtos_em_falta)
    
    st.divider()
    
    # --- RESUMO DE CLIENTES ---
    st.subheader("👥 Base de Clientes")
    clientes = st.session_state.gerenciador_clientes.listar_todos()
    st.metric("Total de Clientes Cadastrados", len(clientes))
    
    st.divider()
    
    # --- RESUMO DE VENDAS ---
    st.subheader("💰 Resumo Financeiro")
    vendas = st.session_state.gerenciador_vendas.listar_todos()
    
    vendas_concluidas = [v for v in vendas if v['status'] == 'concluida']
    valor_total_vendas = sum(float(v['total'] or 0) for v in vendas_concluidas)
    
    col4, col5 = st.columns(2)
    col4.metric("Total de Vendas Concluídas", len(vendas_concluidas))
    col5.metric("Faturamento Total", f"R$ {valor_total_vendas:.2f}")


def main():
    st.title("🛒 Sistema de Supermercado")
    
    st.sidebar.title("Menu")
    pagina = st.sidebar.radio(
        "Navegação",
        ["📦 Produtos", "👥 Clientes", "💰 Vendas","📊 Relatórios"]
    )
    
    if pagina == "📦 Produtos":
        pagina_produtos()
    elif pagina == "👥 Clientes":
        pagina_clientes()
    elif pagina == "💰 Vendas":
        pagina_vendas()
    elif pagina == "📊 Relatórios":
        pagina_relatorios()

if __name__ == "__main__":
    main()