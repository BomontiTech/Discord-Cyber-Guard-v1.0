import discord
from discord.ext import commands
import fade
import os
import time

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

LOGO = """
██████╗ ██╗███████╗ ██████╗ ██████╗ ██████╗ ██████╗ 
██╔══██╗██║██╔════╝██╔════╝██╔═══██╗██╔══██╗██╔══██╗
██║  ██║██║███████╗██║     ██║   ██║██████╔╝██║  ██║
██║  ██║██║╚════██║██║     ██║   ██║██╔══██╗██║  ██║
██████╔╝██║███████║╚██████╗╚██████╔╝██║  ██║██████╔╝
╚═════╝ ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚═════╝ 
         🛡️ BOMONTI CYBER SECURITY GUARD ENGINE v1.0 🛡️
         👑 Developer: Bomonti Automation (SecOps) 👑
"""

# [SİBER AYARLAR] Müşterinin sunucusuna göre ID'ler girilir
GELISMIS_LOG_KANAL_ID = 112233445566778899  # Saldırı engellendiğinde rapor atılacak kanal
SUNUCU_SAHIBI_ID = 123456789012345678       # Botun asla dokunmayacağı güvenli kişi (Kurucu)

@bot.event
async def on_ready():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(fade.purplepink(LOGO))
    print(f"🛡️ [KORUMA AKTİF] '{bot.user.name}' siber savunma modunda 7/24 nöbette!")
    print("=====================================================================")
    print("📢 SİBER KALKAN ÖZELLİKLERİ:")
    print("🔒 Kanal Silme Koruması  -> Aktif")
    print("🔒 Rol Silme Koruması    -> Aktif")
    print("🔒 Sağırlaştırıcı Log    -> Aktif")
    print("=====================================================================\n")

async def yetki_al_ve_raporla(guild, member, eylem_turu, detay):
    """Saldırgan yetkilinin tüm rollerini saniyeler içinde elinden alır"""
    if member.id == SUNUCU_SAHIBI_ID or member.id == guild.owner_id:
        print(f"🛡️ [GÜVENLİ] {member.name} kurucu işlemi onaylandı.")
        return

    print(f"🚨 [SALDIRI TESPİT EDİLDİ] {member.name} tarafından {eylem_turu} gerçekleştirildi!")
    
    # Saldırganın rollerini temizle (Saniyeler içinde yetkisini sıfırla)
    try:
        await member.edit(roles=[], reason="Bomonti Guard: Siber Saldırı Engelleme")
        print(f"🔒 [KİLİTLENDİ] {member.name} adlı kullanıcının tüm yetkileri alındı.")
    except Exception as e:
        print(f"❌ Kullanıcının yetkileri alınamadı (Rolü botun üstünde olabilir): {e}")

    # Log kanalına siber güvenlik raporu gönder
    log_kanali = guild.get_channel(GELISMIS_LOG_KANAL_ID)
    if log_kanali:
        embed = discord.Embed(
            title="🛑 ACİL DURUM: Siber Saldırı Engellendi!",
            description=f"**Saldırgan:** {member.mention} (`{member.id}`)\n**Eylem:** {eylem_turu}\n**Detay:** {detay}",
            color=discord.Color.red()
        )
        embed.add_field(name="🛡️ Alınan Önlem", value="Kullanıcının tüm rolleri elinden alındı ve sunucu emniyete alındı.", inline=False)
        embed.set_footer(text="Bomonti 7/24 AI Shield Protection")
        await log_kanali.send(embed=embed)

@bot.event
async def on_guild_channel_delete(channel):
    """Bir yetkili kanalı sildiği an devreye girer"""
    guild = channel.guild
    async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.channel_delete):
        saldirgan = entry.user
        await yetki_al_ve_raporla(guild, saldirgan, "Kanal Silme", f"Deleted Channel: `#{channel.name}`")

@bot.event
async def on_guild_role_delete(role):
    """Bir yetkili rol sildiği an devreye girer"""
    guild = role.guild
    async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.role_delete):
        saldirgan = entry.user
        await yetki_al_ve_raporla(guild, saldirgan, "Rol Silme", f"Deleted Role: `@{role.name}`")

# [MÜŞTERİ TOKENI] Müşterinin portalından aldığı kod buraya gelecek
TOKEN = "BURAYA_MÜŞTERİNİN_BOT_TOKENİ_GELECEK"

if __name__ == "__main__":
    try:
        bot.run(TOKEN)
    except Exception as e:
        print(f"🛑 [BAĞLANTI HATASI] {e}")
        input()
