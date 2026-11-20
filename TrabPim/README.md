# Rotulação 3D de Tomografia

> Projeto da disciplina **Processamento de Imagem** — Ciência da Computação, UDESC.

## Sobre

Análise de um volume de tomografia (`volume_TAC.pkl`) em que cada voxel representa um tipo de célula. O programa separa os tipos de célula e identifica os agrupamentos (componentes conexos) de cada um com uma rotulação 3D implementada do zero, usando busca em largura (BFS).

## Funcionalidades

- Leitura do volume 3D salvo com `pickle` e exibição do formato e dos valores presentes.
- Separação em três máscaras binárias pelo valor do voxel: **proliferativas** (255), **quiescentes** (200) e **necróticas** (140).
- Rotulação de componentes conexos 3D por BFS, com **conectividade 6** (faces) e **conectividade 26** (faces, arestas e vértices). A busca parte apenas dos voxels de primeiro plano (na mesma ordem da varredura x, y, z), o que deixa a análise do volume 100×100×100 bem mais rápida.
- Para cada tipo de célula e cada conectividade: total de voxels, número de agrupamentos e histograma do tamanho de cada agrupamento.
- Visualização 3D dos voxels rotulados em gráfico de dispersão, apenas quando há menos de 5000 pontos.

## Tecnologias

Python, NumPy, Matplotlib.

## Estrutura

| Arquivo | Descrição |
|---|---|
| `trabPim.py` | Geração de vizinhos 3D, rotulação por BFS e análise. |
| `volume_TAC.pkl` | Volume de tomografia usado como entrada. |

## Como executar

```bash
pip install numpy matplotlib
python trabPim.py
```

O `volume_TAC.pkl` é procurado na pasta do `trabPim.py`, então o programa pode ser executado de qualquer diretório. Os gráficos abrem um de cada vez; feche cada janela para seguir para o próximo.

## Autores

Arthur Bertoli
