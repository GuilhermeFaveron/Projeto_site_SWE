from io import BytesIO

import qrcode
import streamlit as st

st.set_page_config(page_icon="🍔", page_title="PortalBurguer")

cardapio = {
    'Coxinha': {'preco': 6, 'emoji': '🍗'},
    'Risole': {'preco': 7, 'emoji': '🥟'},
    'Bolinho de Queijo': {'preco': 5, 'emoji': '🧀'},
    'Coca lata 350 ml': {'preco': 3.5, 'emoji': '🥤'},
}


def gerar_qrcode(texto):
    imagem = qrcode.make(texto)
    buffer = BytesIO()
    imagem.save(buffer, format='PNG')
    return buffer.getvalue()


if 'carrinho' not in st.session_state:
    st.session_state['carrinho'] = []

if 'finalizado' not in st.session_state:
    st.session_state['finalizado'] = False

st.title('🍔 PortalBurguer')
st.caption('Faça seu pedido e pague pelo QR Code')
st.divider()

item_selecionado = st.selectbox(
    'Escolha um item',
    cardapio.keys(),
    format_func=lambda nome: f"{cardapio[nome]['emoji']} {nome} - R$ {cardapio[nome]['preco']:.2f}",
)

quantidade = st.number_input('Quantidade', min_value=1, step=1)

preco = cardapio[item_selecionado]['preco']

col1, col2 = st.columns(2)

with col1:
    if st.button('Adicionar ao carrinho', use_container_width=True):
        st.session_state['carrinho'].append({
            'item': item_selecionado,
            'emoji': cardapio[item_selecionado]['emoji'],
            'preco': preco,
            'qtd': quantidade,
        })
        st.session_state['finalizado'] = False
        st.toast(f'{item_selecionado} adicionado!', icon='✅')

with col2:
    if st.button('Limpar carrinho', use_container_width=True):
        st.session_state['carrinho'] = []
        st.session_state['finalizado'] = False

st.divider()
st.subheader('🛒 Carrinho')

if not st.session_state['carrinho']:
    st.info('Seu carrinho está vazio.')

for produto in st.session_state['carrinho']:
    subtotal = produto['preco'] * produto['qtd']
    st.write(f"{produto['emoji']} {produto['qtd']}x {produto['item']}: R$ {subtotal:.2f}")

total = sum(p['preco'] * p['qtd'] for p in st.session_state['carrinho'])

st.metric('Total', f'R$ {total:.2f}')

if st.button('Finalizar pedido', type='primary', disabled=not st.session_state['carrinho']):
    st.session_state['finalizado'] = True

if st.session_state['finalizado']:
    st.success('Pedido finalizado! Escaneie o QR Code para pagar.')
    st.image(gerar_qrcode(f'PIX-FICTICIO|PortalBurguer|TOTAL={total:.2f}'), width=220)
    st.caption('QR Code fictício, apenas para demonstração.')