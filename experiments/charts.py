import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

SURF='#fcfcfb'; INK='#0b0b0b'; INK2='#52514e'; MUTED='#8a8880'
BLUE='#2a78d6'; ORANGE='#eb6834'; AQUA='#1baf7a'; GRID='#e8e7e3'
plt.rcParams.update({
    'font.family':'DejaVu Sans','figure.facecolor':SURF,'axes.facecolor':SURF,
    'savefig.facecolor':SURF,'text.color':INK,'axes.edgecolor':GRID,
    'axes.labelcolor':INK2,'xtick.color':INK2,'ytick.color':INK2,
    'axes.spines.top':False,'axes.spines.right':False})

def frame(ax):
    ax.spines['left'].set_visible(False); ax.spines['bottom'].set_color(GRID)
    ax.tick_params(length=0)

def head(ax, title, sub):
    ax.set_title(title, fontsize=16, fontweight='bold', loc='left', pad=34)
    ax.text(0, 1.035, sub, transform=ax.transAxes, fontsize=10.4, color=INK2, va='bottom')

# ---------- 1 ----------
data=[('Árabe',3.50),('Hebraico',3.35),('Turco',3.32),('Latim',3.23),('Português',3.06),
      ('Alemão',3.05),('Grego',2.99),('Latim sem vogais',2.93),('Voynich',2.12)]
labels=[d[0] for d in data][::-1]; vals=[d[1] for d in data][::-1]
cols=[ORANGE if l=='Voynich' else BLUE for l in labels]
fig,ax=plt.subplots(figsize=(9,5.6),dpi=200)
ax.barh(labels, vals, height=0.62, color=cols, zorder=3)
for y,v in enumerate(vals):
    ax.text(v-0.07, y, f'{v:.2f}', va='center', ha='right', color='white',
            fontsize=11, fontweight='bold', zorder=4)
ax.set_xlim(0,4.05); ax.set_xticks([0,1,2,3])
ax.xaxis.grid(True,color=GRID,lw=1,zorder=0); ax.set_axisbelow(True); frame(ax)
for lab in ax.get_yticklabels():
    if lab.get_text()=='Voynich': lab.set_fontweight('bold'); lab.set_color(INK)
head(ax,'Quanto uma letra "prevê" a seguinte',
     'Entropia condicional em bits — medida no mesmo volume de texto (38 mil palavras)')
ax.set_xlabel('bits  ·  menor = mais previsível, mais repetitivo', fontsize=9.8, labelpad=10)
ax.annotate('nenhuma língua chega perto', xy=(2.18,0.02), xytext=(2.42,0.42),
            fontsize=10.2, color=ORANGE, fontweight='bold', ha='left', va='center',
            arrowprops=dict(arrowstyle='-|>',color=ORANGE,lw=1.5,
                            connectionstyle='arc3,rad=0.3',shrinkA=2,shrinkB=3))
plt.tight_layout(); plt.savefig('g1_entropia.png',bbox_inches='tight',pad_inches=0.35); plt.close()

# ---------- 2 ----------
board=[('Grego',-0.024,0.520),('Português',-0.039,0.461),('Latim',-0.028,0.342),
       ('Hebraico',-0.022,0.312),('Alemão',0.071,0.300),('Turco',-0.023,0.210),
       ('Árabe',-0.038,-0.027)]
labels=[b[0] for b in board][::-1]; ctrl=[b[1] for b in board][::-1]; voyv=[b[2] for b in board][::-1]
fig,ax=plt.subplots(figsize=(9,5.9),dpi=200)
y=np.arange(len(labels)); h=0.33
ax.barh(y+h/2+0.025, ctrl, height=h, color=AQUA, zorder=3,
        label='Cifra real (controle) — o ataque quebra')
ax.barh(y-h/2-0.025, voyv, height=h, color=ORANGE, zorder=3,
        label='Voynich — o mesmo ataque falha')
ax.axvline(0,color=INK2,lw=1.2,zorder=4)
for yy,v in zip(y+h/2+0.025, ctrl):
    ax.text(v-0.013 if v<0 else v+0.013, yy, f'{v:+.3f}', va='center',
            ha='right' if v<0 else 'left', fontsize=9, color=INK2)
for yy,v in zip(y-h/2-0.025, voyv):
    ax.text(v+0.013 if v>0 else v-0.013, yy, f'{v:+.3f}', va='center',
            ha='left' if v>0 else 'right', fontsize=9, color=INK2,
            fontweight='bold' if v>0.25 else 'normal')
ax.set_yticks(y); ax.set_yticklabels(labels)
ax.set_xlim(-0.155,0.66); ax.set_ylim(-0.95, len(labels)-0.35)
ax.xaxis.grid(True,color=GRID,lw=1,zorder=0); ax.set_axisbelow(True); frame(ax)
head(ax,'O mesmo ataque quebra cifras reais — e falha no Voynich',
     'Distância até o texto natural depois do ataque automático de decifração')
ax.set_xlabel('défice  ·  0 = língua recuperada   →   maior = mais longe de qualquer língua',
              fontsize=9.8, labelpad=10)
leg=ax.legend(loc='lower right', frameon=False, fontsize=10, handlelength=1.1,
              handleheight=1.1, bbox_to_anchor=(1.0,-0.02))
for t in leg.get_texts(): t.set_color(INK2)
ax.annotate('miragem: passa aqui,\nreprova no dicionário', xy=(-0.045,0.16), xytext=(0.055,0.72),
            fontsize=9.5, color=MUTED, ha='left', va='center',
            arrowprops=dict(arrowstyle='-|>',color=MUTED,lw=1.3,
                            connectionstyle='arc3,rad=-0.3',shrinkA=2,shrinkB=4))
plt.tight_layout(); plt.savefig('g2_placar.png',bbox_inches='tight',pad_inches=0.35); plt.close()

# ---------- 3 ----------
fig,ax=plt.subplots(figsize=(8.4,5.0),dpi=200)
labs=['Voynich','Voynich\n(embaralhado)','Latim']; vals=[16.9,10.3,4.2]
cols=[ORANGE,MUTED,BLUE]
bars=ax.bar(labs,vals,width=0.5,color=cols,zorder=3)
for b,v in zip(bars,vals):
    ax.text(b.get_x()+b.get_width()/2, v+0.6, f'{v:.1f}%', ha='center',
            fontsize=13.5, fontweight='bold', color=INK)
ax.set_ylim(0,21); ax.set_yticks([0,5,10,15,20]); ax.set_yticklabels(['0','5','10','15','20%'])
ax.yaxis.grid(True,color=GRID,lw=1,zorder=0); ax.set_axisbelow(True); frame(ax)
head(ax,'Palavras vizinhas que terminam igual',
     'O texto rima consigo mesmo quatro vezes mais que uma língua real')
ax.text(0.5,-0.20,'ladainha, mantra, encantamento — estrutura de som, não de gramática',
        transform=ax.transAxes, fontsize=9.7, color=MUTED, ha='center', style='italic')
plt.tight_layout(); plt.savefig('g3_eco.png',bbox_inches='tight',pad_inches=0.35); plt.close()
print('ok')
