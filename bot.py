"""
SA-MP Server Status Checker Bot
Discord Bot untuk mengecek status server San Andreas Multiplayer
"""

import discord
from discord import app_commands
from discord.ext import commands
import asyncio
import socket
import struct
import config


class SAMPServerQuery:
    """Class untuk query server SA-MP"""
    
    @staticmethod
    async def query_server(ip: str, port: int):
        """
        Query server SA-MP untuk mendapatkan informasi
        
        Returns:
            dict: Informasi server atau None jika gagal
        """
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(5.0)
            
            query_packet = b'SAMP'
            query_packet += socket.inet_aton(ip)
            query_packet += struct.pack('H', port)
            query_packet += b'i'
            
            loop = asyncio.get_event_loop()
            
            def send_query():
                sock.sendto(query_packet, (ip, port))
                return sock.recvfrom(2048)[0]
            
            data = await asyncio.wait_for(
                loop.run_in_executor(None, send_query),
                timeout=5.0
            )
            
            sock.close()
            
            index = 11
            
            password = data[index]
            index += 1
            
            players = struct.unpack('H', data[index:index+2])[0]
            index += 2
            
            max_players = struct.unpack('H', data[index:index+2])[0]
            index += 2
            
            hostname_len = struct.unpack('I', data[index:index+4])[0]
            index += 4
            
            hostname = data[index:index+hostname_len].decode('cp1252', errors='ignore')
            index += hostname_len
            
            gamemode_len = struct.unpack('I', data[index:index+4])[0]
            index += 4
            
            gamemode = data[index:index+gamemode_len].decode('cp1252', errors='ignore')
            index += gamemode_len
            
            mapname_len = struct.unpack('I', data[index:index+4])[0]
            index += 4
            
            mapname = data[index:index+mapname_len].decode('cp1252', errors='ignore')
            
            return {
                'hostname': hostname,
                'gamemode': gamemode,
                'mapname': mapname,
                'players': players,
                'max_players': max_players,
                'password': bool(password)
            }
            
        except asyncio.TimeoutError:
            return None
        except socket.error:
            return None
        except Exception:
            return None
    
    @staticmethod
    async def query_players(ip: str, port: int):
        """
        Query daftar player dari server SA-MP
        
        Returns:
            list: Daftar player [{'name': str, 'score': int}] atau None
        """
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(5.0)
            
            query_packet = b'SAMP'
            query_packet += socket.inet_aton(ip)
            query_packet += struct.pack('H', port)
            query_packet += b'd'
            
            loop = asyncio.get_event_loop()
            
            def send_query():
                sock.sendto(query_packet, (ip, port))
                return sock.recvfrom(4096)[0]  # Buffer lebih besar untuk banyak player
            
            data = await asyncio.wait_for(
                loop.run_in_executor(None, send_query),
                timeout=5.0
            )
            
            sock.close()
            
            index = 11
            
            player_count = struct.unpack('H', data[index:index+2])[0]
            index += 2
            
            players = []
            
            for _ in range(player_count):
                index += 1  # Skip player ID
                
                name_len = data[index]
                index += 1
                
                name = data[index:index+name_len].decode('cp1252', errors='ignore')
                index += name_len
                
                score = struct.unpack('i', data[index:index+4])[0]
                index += 4
                
                index += 4  # Skip ping
                
                players.append({
                    'name': name,
                    'score': score
                })
            
            return players
            
        except Exception:
            return None


class SAMPServerBot(commands.Bot):
    """Discord Bot untuk cek status server SA-MP"""
    
    def __init__(self):
        intents = discord.Intents.default()
        super().__init__(
            command_prefix=config.COMMAND_PREFIX,
            intents=intents
        )
        self.query = SAMPServerQuery()
    
    async def setup_hook(self):
        """Setup slash commands"""
        # GANTI INI DENGAN ID SERVER KAMU UNTUK SYNC CEPAT!
        MY_GUILD_ID = 1478018137327665212
        await self.tree.sync()
        print("✅ Slash commands synced!")
        
    async def on_ready(self):
        print(f"🤖 Bot {self.user.name} telah online!")
        print(f"🆔 Bot ID: {self.user.id}")
        print(f"🌐 Terhubung ke {len(self.guilds)} server")
        print(f"\n🔗 Invite URL:")
        print(f"https://discord.com/api/oauth2/authorize?client_id={self.user.id}&permissions=2147483648&scope=bot%20applications.commands")
        print("-" * 40)
        
        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name="SA-MP Servers | /ip /players"
            )
        )


bot = SAMPServerBot()


@bot.tree.command(name="ip", description="Cek status server SA-MP")
@app_commands.describe(server_ip="IP Server dengan format ip:port")
async def check_server(interaction: discord.Interaction, server_ip: str):
    await interaction.response.defer(thinking=True)
    
    try:
        if ':' not in server_ip:
            raise ValueError("Format salah")
        
        parts = server_ip.split(':')
        ip = parts[0]
        port = int(parts[1])
        
    except (ValueError, IndexError):
        await interaction.followup.send(
            embed=discord.Embed(
                title="❌ Format Salah",
                description="Format IP harus `ip:port`\nContoh: `51.79.168.190:7777`",
                color=discord.Color.red()
            )
        )
        return
    
    server_info = await bot.query.query_server(ip, port)
    
    if server_info is None:
        error_embed = discord.Embed(
            title="❌ Server Tidak Ditemukan",
            description="Server tidak ditemukan atau sedang offline.",
            color=discord.Color.red()
        )
        error_embed.set_footer(text="SA-MP Server Checker")
        await interaction.followup.send(embed=error_embed)
        return
    
    embed = discord.Embed(
        title="🎮 SA-MP Server Status",
        color=discord.Color.green(),
        timestamp=discord.utils.utcnow()
    )
    
    hostname_display = server_info['hostname'][:50] if len(server_info['hostname']) > 50 else server_info['hostname']
    embed.add_field(name="🏷️ Server Name", value=f"```{hostname_display}```", inline=False)
    embed.add_field(name="🌐 IP Address", value=f"```{server_ip}```", inline=True)
    
    player_percentage = (server_info['players'] / server_info['max_players']) * 100 if server_info['max_players'] > 0 else 0
    player_emoji = "🔴" if player_percentage >= 80 else "🟡" if player_percentage >= 50 else "🟢"
    embed.add_field(name="👥 Players", value=f"```{player_emoji} {server_info['players']}/{server_info['max_players']} ({player_percentage:.1f}%)```", inline=True)
    
    gamemode_display = server_info['gamemode'][:20] if server_info['gamemode'] else "Unknown"
    embed.add_field(name="📊 Game Mode", value=f"```{gamemode_display}```", inline=True)
    
    mapname_display = server_info['mapname'][:20] if server_info['mapname'] else "Unknown"
    embed.add_field(name="🗺️ Map", value=f"```{mapname_display}```", inline=True)
    
    password_status = "🔒 Yes" if server_info['password'] else "🔓 No"
    embed.add_field(name="🔐 Password", value=f"```{password_status}```", inline=True)
    
    embed.set_footer(text="SA-MP Server Checker", icon_url=bot.user.avatar.url if bot.user.avatar else None)
    embed.set_thumbnail(url="https://i.imgur.com/YwH8m3a.png")
    
    await interaction.followup.send(embed=embed)


@bot.tree.command(name="players", description="Lihat daftar player yang online di server SA-MP")
@app_commands.describe(server_ip="IP Server dengan format ip:port")
async def check_players(interaction: discord.Interaction, server_ip: str):
    await interaction.response.defer(thinking=True)
    
    try:
        if ':' not in server_ip:
            raise ValueError("Format salah")
        
        parts = server_ip.split(':')
        ip = parts[0]
        port = int(parts[1])
        
    except (ValueError, IndexError):
        await interaction.followup.send(
            embed=discord.Embed(
                title="❌ Format Salah",
                description="Format IP harus `ip:port`\nContoh: `51.79.168.190:7777`",
                color=discord.Color.red()
            )
        )
        return
    
    server_info = await bot.query.query_server(ip, port)
    
    if server_info is None:
        error_embed = discord.Embed(
            title="❌ Server Tidak Ditemukan",
            description="Server tidak ditemukan atau sedang offline.",
            color=discord.Color.red()
        )
        error_embed.set_footer(text="SA-MP Server Checker")
        await interaction.followup.send(embed=error_embed)
        return
    
    players = await bot.query.query_players(ip, port)
    
    if players is None:
        error_embed = discord.Embed(
            title="❌ Gagal Mengambil Data Player",
            description="Tidak dapat mengambil daftar player.\nServer mungkin memblokir query player.",
            color=discord.Color.orange()
        )
        error_embed.set_footer(text="SA-MP Server Checker")
        await interaction.followup.send(embed=error_embed)
        return
    
    embed = discord.Embed(
        title="👥 Player Online",
        description=f"**{server_info['hostname'][:40]}**\n`{server_ip}`",
        color=discord.Color.blue(),
        timestamp=discord.utils.utcnow()
    )
    
    total_players = len(players)
    
    if total_players == 0:
        embed.add_field(name="📭 Server Kosong", value="Tidak ada player online saat ini.", inline=False)
    else:
        players.sort(key=lambda x: x['score'], reverse=True)
        display_players = players[:25]
        
        player_list = []
        for i, player in enumerate(display_players, 1):
            name = player['name'][:15]
            score = player['score']
            player_list.append(f"`{i:2d}.` {name:<15} │ Score: **{score:,}**")
        
        chunk_size = 15
        chunks = [player_list[i:i + chunk_size] for i in range(0, len(player_list), chunk_size)]
        
        for idx, chunk in enumerate(chunks):
            start = idx * chunk_size + 1
            end = min((idx + 1) * chunk_size, len(display_players))
            field_name = f"🎮 Player ({start}-{end})" if idx == 0 else f"🎮 Player ({start}-{end})"
            embed.add_field(name=field_name, value="\n".join(chunk), inline=False)
        
        if total_players > 25:
            embed.add_field(name="📊 Info", value=f"Menampilkan 25 dari **{total_players}** player", inline=False)
        else:
            embed.add_field(name="📊 Total", value=f"**{total_players}** player online", inline=False)
    
    embed.set_footer(text="SA-MP Server Checker", icon_url=bot.user.avatar.url if bot.user.avatar else None)
    embed.set_thumbnail(url="https://i.imgur.com/YwH8m3a.png")
    
    await interaction.followup.send(embed=embed)


@bot.tree.command(name="ping", description="Cek latency bot")
async def ping(interaction: discord.Interaction):
    latency = round(bot.latency * 1000)
    embed = discord.Embed(title="🏓 Pong!", description=f"Latency: `{latency}ms`", color=discord.Color.blue())
    await interaction.response.send_message(embed=embed)


@bot.command(name="sync")
@commands.is_owner()
async def sync_commands(ctx: commands.Context):
    await ctx.send("🔄 Syncing...")
    synced = await bot.tree.sync()
    await ctx.send(f"✅ Synced {len(synced)} commands globally!")
    
    if ctx.guild:
        bot.tree.copy_global_to(guild=ctx.guild)
        guild_synced = await bot.tree.sync(guild=ctx.guild)
        await ctx.send(f"✅ Synced {len(guild_synced)} commands ke guild ini!")


if __name__ == "__main__":
    if config.DISCORD_TOKEN == "YOUR_BOT_TOKEN_HERE":
        print("❌ ERROR: Token Discord belum diisi!")
        exit(1)
    
    try:
        bot.run(config.DISCORD_TOKEN)
    except discord.LoginFailure:
        print("❌ ERROR: Token Discord tidak valid!")
    except Exception as e:
        print(f"❌ ERROR: {e}")