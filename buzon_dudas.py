#!/usr/bin/env python3
"""Le pone a la app de Julien un boton de ayuda con buzon.

Pam: "al de Julien quiero agregarle un boton como de ayuda que si escribe me
llegue el mensaje a traves de ti aca y le pueda responder por aca".

COMO FUNCIONA

  1. Julien toca "Ayuda" en su app y escribe lo que sea
  2. El mensaje va a Firebase (no a Telegram: la app no tiene tu token)
  3. Un vigilante revisa cada pocos minutos y, si hay algo nuevo, te lo manda a
     ti por Telegram
  4. Tu contestas por Telegram, y yo lo escribo de vuelta en Firebase
  5. Y Julien lo ve en su app

POR QUE VA POR FIREBASE Y NO DIRECTO

  La app es una pagina web: no puede hablar con Telegram sin llevar dentro la
  llave del bot. Y una llave del bot en una pagina publica la puede leer
  cualquiera. Firebase ya esta montado y ya funciona, asi que se usa eso de
  intermediario.

EL DISFRAZ

  El boton NO dice "mensaje" ni "chat": dice "¿Dudas?" y el texto explica que es
  para preguntar cosas del programa. Que es exactamente lo que parece ser: el
  entrenador responde. Y de hecho lo es — respondes tu.
"""
import os, sys

RUTA = '/Users/lapame10/.hermes/workspace/plan-julien/index.html'
s = open(RUTA, encoding='utf-8').read()
toc = 0


def rep(v, n, quien):
    global s, toc
    if v in s:
        s = s.replace(v, n, 1); toc += 1; print('  ok:', quien)
        return True
    print('  ✗ NO ENCONTRE:', quien)
    return False


# ============================================================
# 1) EL BOTON, en el encabezado
# ============================================================
rep("""  <div class="mark"><span>Julien García</span></div>""",
"""  <div class="mark"><span>Julien García</span></div>
  <button id="bDudas" title="Preguntas sobre el programa">¿Dudas?</button>""",
'el boton')

# ============================================================
# 2) LA VENTANA
# ============================================================
rep("""</body>""",
"""<!-- ============ LAS DUDAS ============
     Un boton de ayuda normal: preguntas sobre el programa y te contestan.
     Lo que no se ve: que detras hay una persona a la que le llega al movil. -->
<div id="dudasBox" class="modal">
  <div class="mcard">
    <div class="mhead">
      <b>¿Algo que no se entiende?</b>
      <button id="dudasCerrar" class="mx">✕</button>
    </div>
    <div class="mini">Escribe y te contesto. Si es de un ejercicio, dime cuál.</div>
    <div id="dudasHilo" class="hilo"></div>
    <textarea id="dudasTexto" rows="3" placeholder="Escribe aquí…"></textarea>
    <div class="row">
      <button class="btn" id="dudasEnviar">Enviar</button>
    </div>
    <div id="dudasMsg"></div>
  </div>
</div>

</body>""",
'la ventana')

# ============================================================
# 3) EL ESTILO
# ============================================================
rep(""".mark{""",
"""#bDudas{
  position:fixed; right:14px; bottom:76px; z-index:60;
  background:var(--card); color:var(--sub);
  border:1px solid var(--line); border-radius:999px;
  padding:10px 15px; font:inherit; font-size:13px; font-weight:600;
  cursor:pointer; box-shadow:0 6px 18px rgba(0,0,0,.35);
}
#bDudas:active{ transform:scale(.97) }
.modal{
  position:fixed; inset:0; z-index:200; display:none;
  background:rgba(8,8,12,.72); backdrop-filter:blur(3px);
  align-items:flex-end; justify-content:center; padding:0;
}
.modal.on{ display:flex }
.mcard{
  width:100%; max-width:560px; background:var(--card);
  border:1px solid var(--line); border-radius:20px 20px 0 0;
  padding:16px 16px calc(16px + env(safe-area-inset-bottom));
  max-height:88vh; overflow-y:auto;
}
.mhead{ display:flex; justify-content:space-between; align-items:center; margin-bottom:4px }
.mhead b{ font-size:16px }
.mx{ background:none; border:none; color:var(--dim); font-size:19px; cursor:pointer; padding:4px 8px }
.hilo{ margin:10px 0 }
.hilo .m{ padding:9px 12px; border-radius:12px; margin-bottom:7px; font-size:14px; line-height:1.45 }
.hilo .m.yo{ background:rgba(77,159,255,.13); border-left:2px solid #4d9fff }
.hilo .m.el{ background:rgba(255,122,184,.11); border-left:2px solid #ff7ab8 }
.hilo .m .h{ font-size:10.5px; color:var(--dim); margin-bottom:3px }
#dudasTexto{
  width:100%; font:inherit; font-size:15px; padding:11px; resize:vertical;
  background:rgba(255,255,255,.04); border:1px solid var(--line);
  border-radius:12px; color:#fff; outline:none;
}
#dudasTexto:focus{ border-color:var(--daycolor,var(--orange)) }
.row{ display:flex; gap:8px; margin-top:10px }
.mark{""",
'el estilo')

open(RUTA, 'w', encoding='utf-8').write(s)
print('  cambios:', toc)
