# Nasazení na TrueNAS

Nové repo se klonuje **vedle** staré instalace, ne přes ni.
Stará složka `/mnt/tukieNAS/trading-system` zůstane netknutá jako archiv
(a může to být samostatný dataset, takže ji nepřejmenováváme).

Nová cesta: **`/mnt/tukieNAS/trading`**

Všechny příkazy se spouští v shellu TrueNASu (SSH nebo *System → Shell*).

## 1. Zastavit staré kontejnery

```bash
cd /mnt/tukieNAS/trading-system/compose
docker compose down
```

## 2. Deploy klíč (NAS smí repo jen číst)

```bash
ssh-keygen -t ed25519 -f ~/.ssh/trading_deploy -N "" -C "tukienas-trading"
cat ~/.ssh/trading_deploy.pub
```

Vypsaný veřejný klíč vlož na GitHubu:
repo `trading-system` → *Settings → Deploy keys → Add deploy key*,
**bez** zaškrtnutí *Allow write access*.

Pak řekni SSH, kdy ho použít:

```bash
cat >> ~/.ssh/config <<'EOF'
Host github-trading
  HostName github.com
  User git
  IdentityFile ~/.ssh/trading_deploy
  IdentitiesOnly yes
EOF
chmod 600 ~/.ssh/config
```

## 3. Naklonovat repo

Ideálně si nejdřív v TrueNAS UI vytvoř dataset `tukieNAS/trading`
(*Datasets → Add Dataset*). Pak:

```bash
git clone git@github-trading:tukie8/trading-system.git /mnt/tukieNAS/trading
cd /mnt/tukieNAS/trading
cp .env.example compose/.env
```

## 4. Data a oprávnění

Pokud už máš stažená data ze staré instalace, zkopíruj je (ušetří čas):

```bash
mkdir -p shared/market_data
cp -a /mnt/tukieNAS/trading-system/shared/market_data/. shared/market_data/
```

Kontejner běží jako uživatel s UID 1000, potřebuje zapisovat do runtime složek:

```bash
mkdir -p results/spot_swing_01 bots/spot_swing_01/{logs,state,tmp}
chown -R 1000:1000 shared/market_data results bots/spot_swing_01/logs bots/spot_swing_01/state bots/spot_swing_01/tmp
```

## 5. První běh

```bash
./scripts/download_data.sh            # doplní/stáhne historii 1h + 4h od 2020
./scripts/backtest.sh "baseline"      # první backtest TrendPullbackV1
```

Výsledek opiš jedním řádkem do `docs/EXPERIMENTS.md` (přes PR nebo přímo na GitHubu).

## Aktualizace

Na NASu se nic needituje. Vždy jen:

```bash
cd /mnt/tukieNAS/trading
git pull
```

Pokud `git pull` hlásí lokální změny, někdo editoval na NASu. Změny buď
přesuň do PR, nebo je zahoď (`git checkout -- <soubor>`).

## Dry-run bot (volitelné)

Backtesty kontejner spouští samy. Pokud chceš nechat bota běžet v `dry_run`:

```bash
cd /mnt/tukieNAS/trading/compose
docker compose up -d
docker compose logs -f spot_swing_01
```
