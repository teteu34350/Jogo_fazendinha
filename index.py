import pygame

pygame.init()

# ----- CONFIGURAÇÕES -----
LARGURA, ALTURA = 800, 600
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Fazendinha + Inventário")

FPS = 60
clock = pygame.time.Clock()

# ----- CORES -----
VERDE = (46, 204, 113)
MARROM = (139, 69, 19)
TERRA_UMIDA = (100, 70, 20)
PLANTA = (0, 170, 0)
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
AZUL = (80, 80, 255)

# ----- MAPA -----
TAMANHO_TILE = 50
plantacoes = {}

# ----- FERRAMENTAS -----
FERRAMENTAS = ["MAO", "ENXADA", "REGADOR"]
ferramenta_atual = 0

# ----- INVENTÁRIO -----
inventario = {
    "sementes": 10,
    "colheitas": 0,
    "dinheiro": 0
}

# Fonte
fonte = pygame.font.SysFont("Arial", 20)

def tile_pos(mouse):
    return mouse[0] // TAMANHO_TILE, mouse[1] // TAMANHO_TILE


def desenhar_barra_ferramentas():
    pygame.draw.rect(TELA, PRETO, (0, ALTURA - 60, LARGURA, 60))

    for i, nome in enumerate(FERRAMENTAS):
        x = 10 + i * 160
        y = ALTURA - 50
        cor = AZUL if i == ferramenta_atual else BRANCO
        pygame.draw.rect(TELA, cor, (x, y, 150, 40), 2)
        texto = fonte.render(nome, True, BRANCO)
        TELA.blit(texto, (x + 35, y + 10))


def desenhar_inventario():
    caixa = pygame.Rect(LARGURA - 220, 10, 210, 100)
    pygame.draw.rect(TELA, PRETO, caixa, 2)

    t1 = fonte.render(f"Sementes: {inventario['sementes']}", True, PRETO)
    t2 = fonte.render(f"Colheitas: {inventario['colheitas']}", True, PRETO)
    t3 = fonte.render(f"Dinheiro: ${inventario['dinheiro']}", True, PRETO)

    TELA.blit(t1, (LARGURA - 210, 20))
    TELA.blit(t2, (LARGURA - 210, 50))
    TELA.blit(t3, (LARGURA - 210, 80))


# ----- LOOP PRINCIPAL -----
rodando = True
while rodando:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False

        # TROCAR FERRAMENTA
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                ferramenta_atual = 0
            elif event.key == pygame.K_2:
                ferramenta_atual = 1
            elif event.key == pygame.K_3:
                ferramenta_atual = 2

        # CLICK DO MOUSE (AÇÕES)
        if event.type == pygame.MOUSEBUTTONDOWN:
            tx, ty = tile_pos(pygame.mouse.get_pos())

            if (tx, ty) not in plantacoes:
                plantacoes[(tx, ty)] = {"estado": 0, "molhado": False}

            tile = plantacoes[(tx, ty)]

            # ----- MAO: colher ou limpar -----
            if FERRAMENTAS[ferramenta_atual] == "MAO":
                if tile["estado"] == 3:
                    inventario["colheitas"] += 1
                    plantacoes.pop((tx, ty))
                else:
                    plantacoes.pop((tx, ty))

            # ----- ENXADA: arar ou plantar -----
            elif FERRAMENTAS[ferramenta_atual] == "ENXADA":
                if tile["estado"] == 0:
                    tile["estado"] = 1
                elif tile["estado"] == 1:
                    if inventario["sementes"] > 0:
                        inventario["sementes"] -= 1
                        tile["estado"] = 2

            # ----- REGADOR: molhar ou crescer -----
            elif FERRAMENTAS[ferramenta_atual] == "REGADOR":
                tile["molhado"] = True
                if tile["estado"] == 2:
                    tile["estado"] = 3

    # ----- DESENHAR -----
    TELA.fill(VERDE)

    # Tiles
    for (tx, ty), tile in plantacoes.items():
        x, y = tx * TAMANHO_TILE, ty * TAMANHO_TILE

        if tile["estado"] == 1:
            cor = TERRA_UMIDA if tile["molhado"] else MARROM
            pygame.draw.rect(TELA, cor, (x, y, TAMANHO_TILE, TAMANHO_TILE))

        elif tile["estado"] == 2:
            pygame.draw.rect(TELA, MARROM, (x, y, TAMANHO_TILE, TAMANHO_TILE))
            pygame.draw.circle(TELA, PLANTA, (x + 25, y + 25), 10)

        elif tile["estado"] == 3:
            pygame.draw.rect(TELA, MARROM, (x, y, TAMANHO_TILE, TAMANHO_TILE))
            pygame.draw.circle(TELA, PLANTA, (x + 25, y + 25), 20)

        if tile["molhado"]:
            pygame.draw.circle(TELA, AZUL, (x + 40, y + 40), 6)

    # UI
    desenhar_barra_ferramentas()
    desenhar_inventario()

    pygame.display.update()

pygame.quit()
