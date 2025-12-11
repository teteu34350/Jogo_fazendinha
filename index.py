import pygame
import time

pygame.init()

# ----- CONFIGURAÇÃO DA TELA -----
LARGURA, ALTURA = 800, 600
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Fazendinha")
clock = pygame.time.Clock()

# ----- FONTES / NOTIFICAÇÃO -----
fonte_notif = pygame.font.SysFont("Arial", 24)
fonte_inv = pygame.font.SysFont("Arial", 20)
notificacao_texto = ""
notificacao_tempo = 0

def mostrar_notificacao(texto):
    global notificacao_texto, notificacao_tempo
    notificacao_texto = texto
    notificacao_tempo = time.time()

# ----- INVENTÁRIO -----
inventario = {"Trigo": 0, "Leite": 0}
mostrar_inventario = False
dinheiro = 0

# ----- FASE / NÍVEL -----
fase = 1
max_fase = 4
acoes_para_subir = 2
contador_acoes = 0

# Carregar imagens das fases (tamanho maior)
imagens_fases = [
    pygame.transform.scale(pygame.image.load(f"sprites/nivel{i}.png"), (150, 150))
    for i in range(1, max_fase+1)
]

def aumentar_fase():
    global fase, contador_acoes
    contador_acoes += 1
    if contador_acoes >= acoes_para_subir and fase < max_fase:
        fase += 1
        contador_acoes = 0
        mostrar_notificacao(f"⭐ Você passou para a fase {fase}!")

# ----- FUNDO -----
BACKGROUND = pygame.image.load("sprites/background.png")
BACKGROUND = pygame.transform.scale(BACKGROUND, (LARGURA, ALTURA))

# ----- CASA (CENTRALIZADA) -----
casa_img = pygame.image.load("sprites/casa.png")
casa_img = pygame.transform.scale(casa_img, (200, 160))
casa_largura, casa_altura = 200, 160
casa_x = (LARGURA // 2) - (casa_largura // 2)
casa_y = (ALTURA // 2) - (casa_altura // 2)

# ----- LAGO -----
lago_img = pygame.image.load("sprites/lago.png")
lago_img = pygame.transform.scale(lago_img, (200, 150))
lago_x = LARGURA - 200 - 10
lago_y = ALTURA - 150 - 10

# ----- VENDA -----
venda_img = pygame.image.load("sprites/venda.png")
venda_img = pygame.transform.scale(venda_img, (128, 128))
venda_x = LARGURA - 128 - 10
venda_y = 10
venda_largura = 128
venda_altura = 128

# ----- VACA (3 ESTADOS) -----
vaca_imgs = [
    pygame.transform.scale(pygame.image.load("sprites/vaca-1.png"), (250, 250)),
    pygame.transform.scale(pygame.image.load("sprites/vaca-2.png"), (250, 250)),
    pygame.transform.scale(pygame.image.load("sprites/vaca-3.png"), (250, 250)),
]
vaca_estado, vaca_tempo = 0, 0
vaca_x, vaca_y = 20, ALTURA - 250 - 20

# ----- PERSONAGEM -----
PLAYER_SPRITES = [
    "sprites/fazendeiro-1.png",
    "sprites/fazendeiro-2.png",
    "sprites/fazendeiro-3.png",
    "sprites/fazendeiro-4.png",
]
player_frames = [pygame.transform.scale(pygame.image.load(img), (48, 48)) for img in PLAYER_SPRITES]
player_x, player_y = 300, 300
player_largura, player_altura = 48, 48
velocidade = 3
frame_index, frame_delay, frame_count = 0, 10, 0

# ----- FUNÇÃO DE COLISÃO -----
def colisao(px, py, ox, oy, ow, oh):
    return pygame.Rect(px, py, player_largura, player_altura).colliderect(pygame.Rect(ox, oy, ow, oh))

# ----- CANTEIROS -----
canteiro_img = pygame.image.load("sprites/canteiro-1.png")
canteiro_img = pygame.transform.scale(canteiro_img, (64, 64))
plantio_img = pygame.image.load("sprites/plantio.png")
plantio_img = pygame.transform.scale(plantio_img, (64, 64))
colheita_img = pygame.image.load("sprites/colheita.png")
colheita_img = pygame.transform.scale(colheita_img, (64, 64))

canteiros = [
    {"pos": (0, 0), "estado": "vazio", "tempo": 0},
    {"pos": (64, 0), "estado": "vazio", "tempo": 0},
    {"pos": (0, 64), "estado": "vazio", "tempo": 0},
    {"pos": (64, 64), "estado": "vazio", "tempo": 0},
]

# ----- LOOP PRINCIPAL -----
rodando = True
while rodando:
    agora = time.time()
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

        # INTERAÇÃO CANTEIRO
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_e:
            for c in canteiros:
                cx, cy = c["pos"]
                if colisao(player_x, player_y, cx, cy, 64, 64):
                    if c["estado"] == "vazio":
                        c["estado"] = "plantio"
                        c["tempo"] = agora
                        mostrar_notificacao("🌱 Plantado!")
                    elif c["estado"] == "colheita":
                        c["estado"] = "vazio"
                        inventario["Trigo"] += 1
                        mostrar_notificacao("🧺 Produção colhida! (+1 Trigo)")
                        aumentar_fase()

        # INTERAÇÃO COM A VACA
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_p:
            if colisao(player_x, player_y, vaca_x, vaca_y, 250, 250):
                if vaca_estado == 0:
                    vaca_estado = 1
                    vaca_tempo = agora
                    mostrar_notificacao("🐄 Você alimentou a vaca!")
                elif vaca_estado == 2:
                    inventario["Leite"] += 1
                    mostrar_notificacao("🥛 Você coletou o leite! (+1 Leite)")
                    vaca_estado = 0
                    aumentar_fase()

        # MOSTRAR INVENTÁRIO NA CASA
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_i:
            if colisao(player_x, player_y, casa_x, casa_y, casa_largura, casa_altura):
                mostrar_inventario = not mostrar_inventario

        # VENDER ITENS
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_v:
            if colisao(player_x, player_y, venda_x, venda_y, venda_largura, venda_altura):
                total_vendido = 0
                for item, quantidade in inventario.items():
                    if quantidade > 0:
                        total_vendido += quantidade
                        mostrar_notificacao(f"Você vendeu {quantidade} {item}(s)!")
                        inventario[item] = 0
                        dinheiro += quantidade * 10
                if total_vendido == 0:
                    mostrar_notificacao("Você não tem itens para vender!")

    # MOVIMENTO
    teclas = pygame.key.get_pressed()
    andando = False
    if teclas[pygame.K_w]: player_y -= velocidade; andando = True
    if teclas[pygame.K_s]: player_y += velocidade; andando = True
    if teclas[pygame.K_a]: player_x -= velocidade; andando = True
    if teclas[pygame.K_d]: player_x += velocidade; andando = True
    player_x = max(0, min(LARGURA - player_largura, player_x))
    player_y = max(0, min(ALTURA - player_altura, player_y))
    if andando:
        frame_count += 1
        if frame_count >= frame_delay:
            frame_count = 0
            frame_index = (frame_index + 1) % len(player_frames)
    else:
        frame_index = 0

    # PLANTAS
    for c in canteiros:
        if c["estado"] == "plantio" and agora - c["tempo"] >= 10:
            c["estado"] = "colheita"
            mostrar_notificacao("🌾 A colheita ficou pronta!")

    # VACA
    if vaca_estado == 1 and agora - vaca_tempo >= 10:
        vaca_estado = 2
        mostrar_notificacao("🥛 A vaca produziu leite!")

    # DESENHO NA TELA
    TELA.blit(BACKGROUND, (0, 0))
    TELA.blit(casa_img, (casa_x, casa_y))
    TELA.blit(lago_img, (lago_x, lago_y))
    TELA.blit(venda_img, (venda_x, venda_y))
    TELA.blit(vaca_imgs[vaca_estado], (vaca_x, vaca_y))
    for c in canteiros:
        cx, cy = c["pos"]
        TELA.blit(canteiro_img, (cx, cy))
        if c["estado"] == "plantio": TELA.blit(plantio_img, (cx, cy))
        elif c["estado"] == "colheita": TELA.blit(colheita_img, (cx, cy))
    TELA.blit(player_frames[frame_index], (player_x, player_y))

    # ----- IMAGEM DA FASE CENTRALIZADA -----
    fase_img = imagens_fases[fase-1]
    fase_x = (LARGURA // 2) - (fase_img.get_width() // 2)
    fase_y = 10
    TELA.blit(fase_img, (fase_x, fase_y))

    # NOTIFICAÇÃO
    if notificacao_texto and time.time() - notificacao_tempo < 3:
        caixa = pygame.Surface((LARGURA, 40))
        caixa.set_alpha(180)
        caixa.fill((0, 0, 0))
        TELA.blit(caixa, (0, ALTURA - 50))
        texto_render = fonte_notif.render(notificacao_texto, True, (255, 255, 255))
        TELA.blit(texto_render, (20, ALTURA - 45))

    # INVENTÁRIO
    if mostrar_inventario:
        inv_bg = pygame.Surface((200, 100))
        inv_bg.set_alpha(200)
        inv_bg.fill((50, 50, 50))
        TELA.blit(inv_bg, (LARGURA//2 - 100, ALTURA//2 - 50))
        inv_y = ALTURA//2 - 40
        for item, quantidade in inventario.items():
            texto_inv = f"{item}: {quantidade}"
            render = fonte_inv.render(texto_inv, True, (255, 255, 255))
            TELA.blit(render, (LARGURA//2 - 80, inv_y))
            inv_y += 25

    # DINHEIRO
    dinheiro_render = fonte_inv.render(f"Dinheiro: {dinheiro}", True, (255, 255, 0))
    TELA.blit(dinheiro_render, (10, 10))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
