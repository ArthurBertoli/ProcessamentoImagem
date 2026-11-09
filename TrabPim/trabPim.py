import numpy as np
import pickle
from collections import deque
import matplotlib.pyplot as plt

# 1. FUNÇÃO PARA GERAR VIZINHOS EM 3D
def get_neighbors_3d(x, y, z, shape, connectivity=6):
    """
    Retorna a lista de vizinhos (x,y,z) válidos de um voxel, 
    considerando o tipo de conectividade 3D.
    """
    directions = []
    if connectivity == 6:
        directions = [
            (1, 0, 0), (-1, 0, 0),
            (0, 1, 0), (0, -1, 0),
            (0, 0, 1), (0, 0, -1)
        ]
    elif connectivity == 26:
        # Todas as combinações possíveis exceto o próprio voxel
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                for dz in [-1, 0, 1]:
                    if (dx, dy, dz) != (0, 0, 0):
                        directions.append((dx, dy, dz))
    else:
        raise ValueError("Conectividade deve ser 6 ou 26")

    neighbors = []
    for dx, dy, dz in directions:
        nx, ny, nz = x + dx, y + dy, z + dz
        if 0 <= nx < shape[0] and 0 <= ny < shape[1] and 0 <= nz < shape[2]:
            neighbors.append((nx, ny, nz))
    return neighbors

# 2. FUNÇÃO DE ROTULAÇÃO 3D (BFS)
def label_3d(volume_bin, connectivity=6):
    """
    Rotulação 3D autoral de componentes conexos.
    volume_bin: matriz 3D binária (True/False ou 1/0)
    Retorna:
      labels: matriz 3D com rótulos inteiros (0 = fundo)
      sizes: dicionário com tamanho (n_voxels) de cada rótulo
    """
    labels = np.zeros_like(volume_bin, dtype=np.int32)
    label = 0
    shape = volume_bin.shape
    sizes = {}

    for x in range(shape[0]):
        for y in range(shape[1]):
            for z in range(shape[2]):
                if volume_bin[x, y, z] and labels[x, y, z] == 0:
                    label += 1
                    queue = deque([(x, y, z)])
                    labels[x, y, z] = label
                    count = 1

                    while queue:
                        cx, cy, cz = queue.popleft()
                        for nx, ny, nz in get_neighbors_3d(cx, cy, cz, shape, connectivity):
                            if volume_bin[nx, ny, nz] and labels[nx, ny, nz] == 0:
                                labels[nx, ny, nz] = label
                                queue.append((nx, ny, nz))
                                count += 1

                    sizes[label] = count

    return labels, sizes

# 3. LEITURA DO ARQUIVO DE TOMOGRAFIA
with open("volume_TAC.pkl", "rb") as f:
    volume = pickle.load(f)

print("Volume carregado:", volume.shape)
print("Valores únicos:", np.unique(volume))

# 4. SEPARAÇÃO POR TIPO DE CÉLULA
prolif = (volume == 255)
quiesc = (volume == 200)
necrot = (volume == 140)

# 5. ROTULAÇÃO E ANÁLISE
for name, mask in zip(["Proliferativas", "Quiescentes", "Necróticas"],
                      [prolif, quiesc, necrot]):

    print(f"\n==== {name.upper()} ====")
    print("Total de voxels:", np.sum(mask))

    for conn in [6, 26]:
        labels, sizes = label_3d(mask, connectivity=conn)
        print(f"Conectividade-{conn}: {len(sizes)} agrupamentos detectados")

        # Histograma dos tamanhos
        plt.figure()
        plt.bar(range(1, len(sizes) + 1), list(sizes.values()), color='red')
        plt.title(f"Histograma ({name}) - Conectividade-{conn}")
        plt.xlabel("Agrupamentos")
        plt.ylabel("Volume (nº de voxels)")
        plt.show()

        # Visualização 3D de voxels (apenas exemplo para volumes pequenos)
        coords = np.argwhere(labels > 0)
        if len(coords) < 5000:  # Limita pontos para não travar
            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')
            ax.scatter(coords[:, 0], coords[:, 1], coords[:, 2], c='blue', s=2)
            ax.set_title(f"Volume 3D - {name} (Conectividade-{conn})")
            plt.show()
