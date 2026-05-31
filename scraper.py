best_prices = {}
for code, price_str, volume_str in matches:
    prefix = code[:2]
    if prefix in coffee_codes:
        price = float(price_str.replace(",", ""))
        volume = float(volume_str.replace(",", "")) if volume_str else 0
        if price > 1000 and volume > 0:
            if code not in best_prices or price > best_prices[code][0]:
                best_prices[code] = (price, volume)

for code, (price, volume) in best_prices.items():
    name = get_coffee_name(code)
    print(f"  {code} ({name}): {price:,.0f} ETB | Volume: {volume:,.0f}")
    save_price(code, price, volume)
    found = True