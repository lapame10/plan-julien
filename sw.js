/* ============================================================
   SERVICE WORKER — para que nunca mas sirva una version vieja
   ============================================================
   Por que existe:

   GitHub sirve los archivos con "no me los pidas otra vez en 10 minutos"
   (cache-control: max-age=600). Y si la app esta puesta en la pantalla de inicio
   del movil, esa entrada del icono ni siquiera lleva la marca de version.

   Resultado: Pam publica algo, lo prueba, y sigue viendo lo de antes. Y cree
   —con razon— que no se ha publicado. Ya paso con la bitacora de ThermalApp.

   La solucion: ESTE archivo se pone en medio. Y funciona al reves de lo normal:

     - con conexion: va a internet SIEMPRE, y de paso guarda la copia nueva
     - sin conexion: tira de la copia guardada

   Asi, con cobertura, ve lo ultimo que se publico. Sin esperar, sin recargar dos
   veces, sin borrar el icono.

   ⚠️ Y lo que NO se toca nunca:
     - Firebase (los datos, el buzon, los logs): siempre a la red, jamas cacheado.
       Si se cacheara, Julien veria sus series viejas y el aviso no llegaria.
   ============================================================ */

const VERSION = 'julien-v1';

self.addEventListener('install', (e) => {
  /* en cuanto se instala, toma el control sin esperar a que cierren la pestaña */
  self.skipWaiting();
});

self.addEventListener('activate', (e) => {
  e.waitUntil(
    (async () => {
      /* borrar las copias de versiones anteriores */
      const nombres = await caches.keys();
      await Promise.all(
        nombres.filter(n => n.startsWith('julien-') && n !== VERSION).map(n => caches.delete(n))
      );
      await self.clients.claim();
    })()
  );
});

self.addEventListener('fetch', (e) => {
  const req = e.request;
  const url = new URL(req.url);

  if (req.method !== 'GET') return;

  /* ===== LOS DATOS, NUNCA C ACHEADOS =====
     Firebase y cualquier cosa que no sea del propio sitio: directo a la red. */
  if (url.origin !== self.location.origin) return;

  /* ===== LO DEL PROPIO SITIO: RED PRIMERO ===== */
  e.respondWith(
    (async () => {
      try {
        const r = await fetch(req, { cache: 'no-store' });
        /* se guarda la copia nueva para poder usarla sin conexion */
        if (r && r.ok) {
          const copia = r.clone();
          caches.open(VERSION).then(c => c.put(req, copia)).catch(() => {});
        }
        return r;
      } catch (err) {
        /* sin conexion: lo ultimo que se guardo */
        const guardada = await caches.match(req);
        if (guardada) return guardada;
        throw err;
      }
    })()
  );
});
