from app.db.models.product import Product


def render_product_text(product: Product) -> str:
    parts = [
        f"💍 <b>{product.name}</b>",
        f"\n💰 <b>Цена:</b> {product.price} ₽",
    ]

    if product.weight:
        parts.append(f"⚖️ <b>Вес:</b> {product.weight}")

    if product.size:
        parts.append(f"📏 <b>Размер:</b> {product.size}")

    if product.inserts:
        parts.append(f"💎 <b>Вставки:</b> {product.inserts}")

    if product.metal:
        parts.append(f"🔗 <b>Металл:</b> {product.metal}")

    if product.uin:
        parts.append(f"🆔 <b>УИН:</b> {product.uin}")

    if product.description:
        parts.append(f"\n📝 {product.description}")

    return "\n".join(parts)
