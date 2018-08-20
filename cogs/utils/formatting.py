import discord

def format_simple_embed(title, desc, color, footer_text = None, footer_icon = None):
    embed = discord.Embed(title=title, description=desc, color=color)
    if footer_text and footer_icon:
        embed.set_footer(text=footer_text, icon_url=footer_icon)

    return embed

def format_generic_success(title, desc):
    return format_simple_embed(title=title,
                               desc=desc,
                               color=discord.Color.green())

def format_generic_error(title, desc):
    return format_simple_embed(title=title,
                               desc=desc,
                               color=discord.Color.from_rgb(255,0,0))