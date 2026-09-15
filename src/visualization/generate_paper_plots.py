"""
Generate publication-quality figures for Springer LNCS paper.
Follows Springer guidelines: grayscale-safe, Computer Modern fonts,
clean axes, no chartjunk, proper sizing for single-column (84mm) or
double-column (174mm) width at 300+ DPI.
"""

import matplotlib
matplotlib.use('Agg')  # non-interactive backend
import matplotlib.pyplot as plt
import numpy as np

# ── Springer LNCS styling ──────────────────────────────────────────
plt.rcParams.update({
    'font.family': 'serif',
    'font.serif': ['Times New Roman', 'DejaVu Serif', 'serif'],
    'font.size': 9,
    'axes.titlesize': 10,
    'axes.labelsize': 9,
    'xtick.labelsize': 8,
    'ytick.labelsize': 8,
    'legend.fontsize': 8,
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
    'savefig.pad_inches': 0.05,
    'axes.linewidth': 0.6,
    'xtick.major.width': 0.5,
    'ytick.major.width': 0.5,
    'xtick.major.size': 3,
    'ytick.major.size': 3,
    'axes.grid': True,
    'grid.alpha': 0.3,
    'grid.linewidth': 0.4,
    'axes.spines.top': False,
    'axes.spines.right': False,
})

# ── Data ────────────────────────────────────────────────────────────
models = [
    'GPT-5.6\nLuna',
    'Gemini 3.1\nFlash Lite',
    'Gemini 2.5\nFlash',
    'Qwen 3.5\nFlash',
    'DeepSeek\nV4 Flash',
    'Qwen 3.6\n27B',
    'GPT-4o\nMini',
    'LLaMA 3.3\n70B',
]

en_r1   = [24.12, 22.94, 22.13, 21.99, 21.43, 21.31, 21.16, 20.38]
bn_r1   = [14.01, 14.04, 15.05, 14.74, 15.00, 13.50, 15.63, 16.23]

# BanglaSummEval (sorted by F1 descending for the second chart)
bse_models = [
    'Gemini 2.5\nFlash',
    'LLaMA 3.3\n70B',
    'DeepSeek\nV4 Flash',
    'GPT-4o\nMini',
    'Qwen 3.6\n27B',
    'Qwen 3.5\nFlash',
    'GPT-5.6\nLuna',
    'Gemini 3.1\nFlash Lite',
]
precision = [61.65, 65.78, 64.14, 63.38, 60.49, 61.48, 58.87, 52.83]
recall    = [60.83, 57.50, 56.17, 55.33, 59.00, 57.17, 56.17, 52.50]
f1        = [58.43, 58.28, 57.34, 56.73, 56.41, 56.15, 54.84, 49.73]

# Grayscale-safe hatching patterns + distinct fills
BLUE   = '#2b5c8f'
ORANGE = '#d95f02'
GREEN  = '#1b7837'
PURPLE = '#762a83'
RED    = '#c0392b'


# ── Figure 1: Cross-Lingual ROUGE-1 ────────────────────────────────
def fig_rouge():
    # Springer double-column width ≈ 174 mm ≈ 6.85 in
    fig, ax = plt.subplots(figsize=(6.85, 3.2))

    x = np.arange(len(models))
    w = 0.32

    bars_en = ax.bar(x - w/2, en_r1, w,
                     color=BLUE, edgecolor='black', linewidth=0.4,
                     label='English', zorder=3)
    bars_bn = ax.bar(x + w/2, bn_r1, w,
                     color=ORANGE, edgecolor='black', linewidth=0.4,
                     hatch='///', label='Bengali', zorder=3)

    # Value labels
    for b in bars_en:
        ax.text(b.get_x() + b.get_width()/2, b.get_height() + 0.3,
                f'{b.get_height():.1f}', ha='center', va='bottom', fontsize=7)
    for b in bars_bn:
        ax.text(b.get_x() + b.get_width()/2, b.get_height() + 0.3,
                f'{b.get_height():.1f}', ha='center', va='bottom', fontsize=7)

    ax.set_ylabel('ROUGE-1 F$_1$ (%)')
    ax.set_xticks(x)
    ax.set_xticklabels(models, fontsize=7.5)
    ax.set_ylim(0, 28)
    ax.legend(loc='upper right', frameon=True, edgecolor='gray',
              fancybox=False, framealpha=1)

    fig.savefig('figures/fig_cross_lingual_rouge.png')
    fig.savefig('figures/fig_cross_lingual_rouge.pdf')
    print('[OK] figures/fig_cross_lingual_rouge  (.png + .pdf)')
    plt.close(fig)


# ── Figure 2: BanglaSummEval Factuality ─────────────────────────────
def fig_banglasummeval():
    fig, ax = plt.subplots(figsize=(6.85, 3.4))

    x = np.arange(len(bse_models))
    w = 0.28

    ax.bar(x - w, precision, w,
           color=GREEN, edgecolor='black', linewidth=0.4,
           label='Precision (Factuality)', zorder=3)
    ax.bar(x,     recall,    w,
           color=PURPLE, edgecolor='black', linewidth=0.4,
           hatch='///', label='Recall (Coverage)', zorder=3)
    ax.bar(x + w, f1,        w,
           color=RED, edgecolor='black', linewidth=0.4,
           hatch='xxx', label='F1 Score', zorder=3)

    # F1 value labels on top of the red bars
    for i, v in enumerate(f1):
        ax.text(x[i] + w, v + 0.5, f'{v:.1f}', ha='center', va='bottom',
                fontsize=7, fontweight='bold')

    ax.set_ylabel('Score (%)')
    ax.set_xticks(x)
    ax.set_xticklabels(bse_models, fontsize=7.5)
    ax.set_ylim(45, 72)
    ax.legend(loc='upper right', frameon=True, edgecolor='gray',
              fancybox=False, framealpha=1, ncol=1)

    fig.savefig('figures/fig_banglasummeval_factuality.png')
    fig.savefig('figures/fig_banglasummeval_factuality.pdf')
    print('[OK] figures/fig_banglasummeval_factuality  (.png + .pdf)')
    plt.close(fig)


# ── Figure 3 (bonus): Radar / Spider chart — Bengali metric profile ─
def fig_radar():
    """Radar chart comparing top-3 Bengali models across all metrics."""
    categories = ['ROUGE-1', 'ROUGE-2', 'ROUGE-L', 'BLEU', 'chrF', 'BERTScore-R']

    # Normalised to [0,1] within each metric's range for visual clarity
    raw = {
        'LLaMA 3.3 70B':  [16.23, 5.29, 12.44, 1.90, 33.30, 87.94],
        'Gemini 2.5 Flash': [15.05, 4.32, 11.27, 1.64, 33.11, 87.93],
        'GPT-4o Mini':     [15.63, 4.53, 11.83, 1.74, 33.74, 87.80],
    }
    # min-max per metric across ALL 8 models for scaling
    mins = [13.50, 3.57, 10.11, 0.98, 28.38, 87.44]
    maxs = [16.23, 5.29, 12.44, 1.90, 33.74, 87.94]

    N = len(categories)
    angles = np.linspace(0, 2*np.pi, N, endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(4.5, 4.5), subplot_kw=dict(polar=True))

    colors = [BLUE, ORANGE, GREEN]
    markers = ['o', 's', '^']
    for idx, (name, vals) in enumerate(raw.items()):
        normed = [(v - mn) / (mx - mn) if mx != mn else 0.5
                  for v, mn, mx in zip(vals, mins, maxs)]
        normed += normed[:1]
        ax.plot(angles, normed, linewidth=1.4, marker=markers[idx],
                markersize=4, label=name, color=colors[idx])
        ax.fill(angles, normed, alpha=0.08, color=colors[idx])

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=8)
    ax.set_ylim(0, 1.15)
    ax.set_yticks([0.25, 0.5, 0.75, 1.0])
    ax.set_yticklabels(['25%', '50%', '75%', '100%'], fontsize=6, color='gray')
    ax.legend(loc='upper right', bbox_to_anchor=(1.35, 1.12), frameon=True,
              edgecolor='gray', fancybox=False, fontsize=7.5)

    fig.savefig('figures/fig_radar_bengali.png')
    fig.savefig('figures/fig_radar_bengali.pdf')
    print('[OK] figures/fig_radar_bengali  (.png + .pdf)')
    plt.close(fig)


# ── Main ────────────────────────────────────────────────────────────
if __name__ == '__main__':
    fig_rouge()
    fig_banglasummeval()
    fig_radar()
    print('\nAll Springer-ready figures generated.')
