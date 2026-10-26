# O Prontuário · Manual da rotina diária

Este manual é lido pela tarefa agendada que produz e publica os posts do @oprontuario.med. Siga à risca.

## Peças do sistema

| Peça | Onde | Para quê |
| --- | --- | --- |
| Repositório | `mindmed0123/prontu-rio.med` | Kit de produção (`kit/`) e imagens publicadas (`midia/AAAA-MM-DD/<slug>/`) |
| ClickUp | Lista **✅ Aprovação diária** (id `1600200000001006`) | Pedro aprova cada post |
| Windsor.ai | Conector `instagram`, conta `17841417732167045` | Publica no Instagram |
| Link público das imagens | `https://raw.githubusercontent.com/mindmed0123/prontu-rio.med/main/<caminho>` | A API do Instagram exige URL pública de JPEG |

Status da lista: `para aprovar` → `aprovado` → `publicado`. Também existem `ajustar` (Pedro pediu mudança nos comentários), `sugestão` (tema sugerido por Pedro) e `descartado`.

## Identidade visual (não negociável)

- **Fonte da marca:** Instrument Serif, a mesma do P do logo. Todo título e todo "O Prontuário" usam essa fonte. Texto corrido em Inter Tight. Rótulos pequenos em JetBrains Mono.
- **Cores:** tinta `#0E1A1F`, papel `#F3F0E8`, verde `#2EC4A6`, verde escuro `#1F7A6A`.
- **Carrossel:** sempre pelo `template-carrossel.html` via `gen.py`. Não altere CSS, classes ou ordem. A tarja do meio da capa usa a itálica da mesma família, como no template aprovado.
- **Imagens em alta resolução, sem ampliar.** O `gen.py` imprime `scale`: precisa ser ≤ 1 em todas as imagens. Se passar de 1, troque a foto.
- **Capa chamativa:** político, autoridade ou rosto conhecido ligado ao tema sempre que houver foto livre (Agência Senado, STF, Câmara, Planalto no Flickr). Senão, uma foto forte e específica do tema.
- Nada de rosto coberto pelas tarjas da capa (elas ocupam de y≈860 a y≈1165). Logo "O Prontuário" no topo precisa ficar legível; use `topshade` ou estenda o fundo.

## Fotos: licença e origem

- **Permitido:** Flickr com licença 4, 5, 9, 10, 11, 12 (CC BY, CC BY-SA, CC0, domínio público); Pexels; Wikimedia Commons com licença livre; NIH/NIAID (domínio público).
- **Proibido:** licença 0 (todos os direitos reservados), NC (não comercial), imagens de veículos de imprensa, Google Imagens.
- **Flickr:** `python3 kit/flickr.py <pasta> <url-da-foto>...` baixa pelo proxy `i0.wp.com` (o Flickr bloqueia download direto) e imprime a licença.
- **Pexels:** `https://images.pexels.com/photos/ID/pexels-photo-ID.jpeg?auto=compress&cs=tinysrgb&w=2600`.
- **Commons:** `https://i0.wp.com/upload.wikimedia.org/wikipedia/commons/{h[0]}/{h[:2]}/{nome}?w=3000`, com `h = md5(nome_com_underscores)`.
- Busca: use a busca do Flickr (`flickr.com/search/?text=...&license=4,5,9,10,11,12`), Pexels ou a API do Commons. Confira visualmente cada foto antes de usar: o tema tem de bater (já houve foto rotulada errada no Commons).
- Crédito das fotos sempre no fim da legenda.

## Rigor editorial

- Notícias das últimas 48 horas, com fonte primária aberta e lida: resolução, artigo, comunicado oficial ou veículo sério (Folha, Estadão, Valor, O Globo, Poder360, Agência Senado, Agência Câmara, Futuro da Saúde, Medicina S/A, JAMA, NEJM, Lancet, BMJ, PubMed).
- Confira cada número, nome, cargo e data na fonte. Se não confirmar, não use. Exemplo de erro já cometido: chamar de "médico" um senador que não é médico.
- Temas políticos: mostrar os dois lados e incluir "O Prontuário não apoia candidatos."
- Nunca dar conduta clínica para paciente. O público é médico.
- Não repetir tema publicado nos últimos 14 dias. Consulte os cartões `publicado` da lista.

## Mix diário (5 posts)

1. Carrossel de notícia · Carreira e Regulação (CFM, CRM, honorários, residência, Enamed)
2. Carrossel de notícia · Mercado (SUS, ANS, hospitais, operadoras, política de saúde)
3. Carrossel "estudo em 1 minuto" · Ciência (artigo recente, com números e limitações)
4. Carrossel de notícia · o tema mais forte do dia, de qualquer editoria (de preferência delicado ou viral, com rigor)
5. Quiz do plantão ou "número do dia", em carrossel de 2 slides (modelos em `kit/exemplos/posts-simples-quiz-numero.html`, renderizados por `kit/render-posts.js`)

Se houver cartão com status `sugestão`, priorize o tema sugerido e mova esse cartão para `descartado` com o comentário "virou post de DD/MM".

Horários de publicação: 07h, 10h, 12h, 17h e 20h. Distribua os 5 posts nesses horários, o mais forte às 12h.

## Como produzir cada carrossel

1. Escreva capa (3 tarjas curtas), 3 slides (manchete até ~65 caracteres, texto até ~200 caracteres) e a legenda (gancho na primeira linha, contexto, pergunta para comentários, "Link na bio", créditos, 6 a 8 hashtags, sempre `#oprontuario`).
2. Baixe as fotos para uma pasta de trabalho.
3. Monte o JSON como em `kit/exemplos/` e rode:
   ```
   python3 kit/gen.py config.json
   cd <pasta com node_modules do playwright> && node kit/render-carrossel.js /tmp/carrossel.html <pasta-de-saida>
   ```
   Saída: 5 PNG 1080x1350. `render-carrossel.js` imprime as alturas de título e texto; título com mais de 2 linhas (altura > 130) deve ser encurtado.
4. Olhe cada slide renderizado (capa inteira em tamanho real). Corrija enquadramento e texto até ficar no padrão.
5. Converta para JPEG qualidade 95 (`subsampling=0`), menos de 8 MB cada, salve em `midia/AAAA-MM-DD/<slug>/01-capa.jpg` etc., faça commit e push.
6. Confirme que cada URL raw responde `200 image/jpeg`.

## Cartão no ClickUp

- Nome: `HHh · <título curto> · carrossel` (ex.: `12h · Tabela SUS: o que cada lado promete · carrossel`).
- Status: `para aprovar`. Data de entrega (due date): o horário de publicação do dia.
- Descrição em Markdown, nesta ordem: imagens embutidas `![](url)` de todos os slides; `### Legenda` com o texto exato; `### Fontes` com os links; e no fim o bloco de máquina:
  ```
  <!-- PUBLICAR
  tipo: carousel
  imagens:
  <url 1>
  <url 2>
  ...
  -->
  ```

## Publicação

Para cada cartão `aprovado` cujo horário já chegou:
1. Leia a descrição completa. Pegue as URLs do bloco `PUBLICAR` (sem colchetes de link) e a legenda da seção `### Legenda`.
2. Publique com Windsor `execute_action`: connector `instagram`, account `17841417732167045`, action `create_carousel_post` (ou `create_image_post` para imagem única), params `image_urls` e `caption`.
3. Se der certo: mova para `publicado` e comente o media id. Se der erro: mantenha `aprovado`, comente o erro e tente na próxima janela. Erro de permissão do Instagram significa reconectar em `onboard.windsor.ai/app/instagram` pela opção "Connect with Facebook instead", o que só o Pedro pode fazer.
4. Cartões em `ajustar`: aplique o que Pedro pediu nos comentários, rerenderize, atualize imagens e descrição e volte para `para aprovar`.
