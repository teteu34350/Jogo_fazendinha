import pygame
import time

pygame.init()

LARGURA, ALTURA = 800, 600
TELA = pygame.display.set_mode((LARGURA, ALTURA))
clock = pygame.time.Clock()

# ----- FUNDO -----
BACKGROUND = pygame.image.load("Jogo_fazendinha/sprites/background.png")
BACKGROUND = pygame.transform.scale(BACKGROUND, (LARGURA, ALTURA))

# ----- CASA -----
casa_img = pygame.image.load("Jogo_fazendinha/sprites/casa.png")
casa_img = pygame.transform.scale(casa_img, (200, 160))
casa_x = (LARGURA // 2) - 100
casa_y = 10

# ----- LAGO -----
lago_img = pygame.image.load("Jogo_fazendinha/sprites/lago.png")
lago_img = pygame.transform.scale(lago_img, (200, 150))

lago_x = LARGURA - 200 - 10   # canto direito
lago_y = ALTURA - 150 - 10    # canto inferior

# ----- VACA (3 ESTADOS) -----
vaca_imgs = [
    pygame.transform.scale(pygame.image.load("Jogo_fazendinha/sprites/vaca-1.png"), (250, 250)),  # normal
    pygame.transform.scale(pygame.image.load("Jogo_fazendinha/sprites/vaca-2.png"), (250, 250)),  # comendo
    pygame.transform.scale(pygame.image.load("Jogo_fazendinha/sprites/vaca-3.png"), (250, 250)),  # leite pronto
]

vaca_estado = 0
vaca_tempo = 0
vaca_x = 20
vaca_y = ALTURA - 250 - 20

# ----- PERSONAGEM -----
PLAYER_SPRITES = [
    "Jogo_fazendinha/sprites/fazendeiro-1.png",
    "Jogo_fazendinha/sprites/fazendeiro-2.png",
    "Jogo_fazendinha/sprites/fazendeiro-3.png",
    "Jogo_fazendinha/sprites/fazendeiro-4.png",
]

player_frames = [
    pygame.transform.scale(pygame.image.load(img), (48, 48))
    for img in PLAYER_SPRITES
]

player_x = 300
player_y = 300
player_largura = 48
player_altura = 48
velocidade = 3

frame_index = 0
frame_delay = 10
frame_count = 0

def colisao(px, py, ox, oy, ow, oh):
    area_player = pygame.Rect(px, py, player_largura, player_altura)
    area_obj = pygame.Rect(ox, oy, ow, oh)
    return area_player.colliderect(area_obj)

# ----- CANTEIROS -----
canteiro_img = pygame.image.load("Jogo_fazendinha/sprites/canteiro-1.png")
canteiro_img = pygame.transform.scale(canteiro_img, (64, 64))

plantio_img = pygame.image.load("Jogo_fazendinha/sprites/plantio.png")
plantio_img = pygame.transform.scale(plantio_img, (64, 64))

colheita_img = pygame.image.load("Jogo_fazendinha/sprites/colheita.png")
colheita_img = pygame.transform.scale(colheita_img, (64, 64))

canteiros = [
    {"pos": (0, 0),   "estado": "vazio", "tempo": 0},
    {"pos": (64, 0),  "estado": "vazio", "tempo": 0},
    {"pos": (0, 64),  "estado": "vazio", "tempo": 0},
    {"pos": (64, 64), "estado": "vazio", "tempo": 0},
]

rodando = True
while rodando:
    agora = time.time()

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

        # ----- INTERAÇÃO CANTEIRO -----
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_e:
            for c in canteiros:
                cx, cy = c["pos"]
                if colisao(player_x, player_y, cx, cy, 64, 64):

                    if c["estado"] == "vazio":
                        c["estado"] = "plantio"
                        c["tempo"] = agora
                        print("🌱 Plantado!")

                    elif c["estado"] == "colheita":
                        c["estado"] = "vazio"
                        print("🧺 Colhido!")

        # ----- INTERAÇÃO COM A VACA -----
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_p:
            if colisao(player_x, player_y, vaca_x, vaca_y, 250, 250):

                if vaca_estado == 0:
                    vaca_estado = 1
                    vaca_tempo = agora
                    print("🐄 Você alimentou a vaca!")

                elif vaca_estado == 2:
                    print("🥛 Você coletou o leite!")
                    vaca_estado = 0

    # ----- CONTROLE DE MOVIMENTO -----
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

    # ----- PLANTAS -----
    for c in canteiros:
        if c["estado"] == "plantio" and agora - c["tempo"] >= 10:
            c["estado"] = "colheita"
            print("🌾 Colheita pronta!")

    # ----- VACA -----
    if vaca_estado == 1 and agora - vaca_tempo >= 10:
        vaca_estado = 2
        print("🥛 A vaca produziu leite!")

    # ============================
    # ----- DESENHO NA TELA -----
    # ============================

    TELA.blit(BACKGROUND, (0, 0))

    # Casa
    TELA.blit(casa_img, (casa_x, casa_y))

    # Lago (NOVO)
    TELA.blit(lago_img, (lago_x, lago_y))

    # Vaca
    TELA.blit(vaca_imgs[vaca_estado], (vaca_x, vaca_y))

    # Canteiros
    for c in canteiros:
        cx, cy = c["pos"]
        TELA.blit(canteiro_img, (cx, cy))
        if c["estado"] == "plantio":
            TELA.blit(plantio_img, (cx, cy))
        elif c["estado"] == "colheita":
            TELA.blit(colheita_img, (cx, cy))

    # Player
    TELA.blit(player_frames[frame_index], (player_x, player_y))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
