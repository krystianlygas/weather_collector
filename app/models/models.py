# coding: utf-8
from sqlalchemy import Boolean, CHAR, Column, Date, DateTime, ForeignKey, Integer, Numeric, String, Text, UniqueConstraint, text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class FlywaySchemaHistory(Base):
    __tablename__ = 'flyway_schema_history'

    installed_rank = Column(Integer, primary_key=True)
    version = Column(String(50))
    description = Column(String(200), nullable=False)
    type = Column(String(20), nullable=False)
    script = Column(String(1000), nullable=False)
    checksum = Column(Integer)
    installed_by = Column(String(100), nullable=False)
    installed_on = Column(DateTime, nullable=False, server_default=text("now()"))
    execution_time = Column(Integer, nullable=False)
    success = Column(Boolean, nullable=False, index=True)


class Jednostka(Base):
    __tablename__ = 'jednostka'

    id_jednostka = Column(Numeric(6, 0), primary_key=True)
    jednostka_nazwa_skrot = Column(String(50))
    jednostka_nazwa_pelna = Column(String(150))


class Kraj(Base):
    __tablename__ = 'kraj'

    id_kraj = Column(Numeric(3, 0), primary_key=True)
    kraj_kod = Column(CHAR(2))
    kraj_nazwa = Column(String(75))


class ProfilCzasNastaw(Base):
    __tablename__ = 'profil_czas_nastaw'

    id_profil_czas = Column(Numeric(10, 0), primary_key=True)
    profil_nazwa = Column(String(50), nullable=False)
    liczba_dni_wstecz = Column(Numeric(2, 0))
    liczba_godzin_wstecz = Column(Numeric(3, 0))


class Role(Base):
    __tablename__ = 'role'

    id_rola = Column(Numeric(1, 0), primary_key=True)
    rola_nazwa = Column(String(15))


class SocialaccountSocialapp(Base):
    __tablename__ = 'socialaccount_socialapp'

    id = Column(Integer, primary_key=True, server_default=text("nextval('socialaccount_socialapp_id_seq'::regclass)"))
    provider = Column(String(30), nullable=False)
    name = Column(String(40), nullable=False)
    client_id = Column(String(191), nullable=False)
    secret = Column(String(191), nullable=False)
    key = Column(String(191), nullable=False)


class TypModul(Base):
    __tablename__ = 'typ_modul'

    id_typ_modul = Column(Numeric(1, 0), primary_key=True)
    nazwa_typ_modul = Column(String(30))
    czy_modyfikacja = Column(Boolean, server_default=text("true"))


class UsersUser(Base):
    __tablename__ = 'users_user'

    id = Column(Integer, primary_key=True, server_default=text("nextval('users_user_id_seq'::regclass)"))
    password = Column(String(128), nullable=False)
    last_login = Column(DateTime(True))
    is_superuser = Column(Boolean, nullable=False)
    username = Column(String(150), nullable=False, unique=True)
    first_name = Column(String(30), nullable=False)
    last_name = Column(String(150), nullable=False)
    email = Column(String(254), nullable=False)
    is_staff = Column(Boolean, nullable=False)
    is_active = Column(Boolean, nullable=False)
    date_joined = Column(DateTime(True), nullable=False)
    name = Column(String(255), nullable=False)


class Modul(Base):
    __tablename__ = 'modul'

    id_modul = Column(Numeric(6, 0), primary_key=True)
    modul_nazwa = Column(String(75))
    modul_sn = Column(String(12))
    id_typ_modul = Column(ForeignKey('typ_modul.id_typ_modul'))
    czy_aktywne = Column(Boolean, server_default=text("true"))

    typ_modul = relationship('TypModul')


class SocialaccountSocialaccount(Base):
    __tablename__ = 'socialaccount_socialaccount'
    __table_args__ = (
        UniqueConstraint('provider', 'uid'),
    )

    id = Column(Integer, primary_key=True, server_default=text("nextval('socialaccount_socialaccount_id_seq'::regclass)"))
    provider = Column(String(30), nullable=False)
    uid = Column(String(191), nullable=False)
    last_login = Column(DateTime(True), nullable=False)
    date_joined = Column(DateTime(True), nullable=False)
    extra_data = Column(Text, nullable=False)
    user_id = Column(ForeignKey('users_user.id', deferrable=True, initially='DEFERRED'), nullable=False, index=True)

    user = relationship('UsersUser')


class Uzytkownik(Base):
    __tablename__ = 'uzytkownik'

    id_uzytkownik = Column(Numeric(6, 0), primary_key=True)
    imie = Column(String(30))
    nazwisko = Column(String(30))
    email_uzytkownik = Column(String(50))
    login_uzytkownik = Column(String(20))
    haslo_uzytkownik = Column(String(60))
    jest_aktywny = Column(Boolean)
    id_jednostka = Column(ForeignKey('jednostka.id_jednostka'))
    id_rola = Column(ForeignKey('role.id_rola'))

    jednostka = relationship('Jednostka')
    role = relationship('Role')


class Wojewodztwo(Base):
    __tablename__ = 'wojewodztwo'

    id_wojewodztwo = Column(Numeric(4, 0), primary_key=True)
    wojewodztwo_nazwa_pelna = Column(String(50))
    wojewodztwo_nazwa_skrot = Column(String(10))
    id_kraj = Column(ForeignKey('kraj.id_kraj'))

    kraj = relationship('Kraj')


class Miasto(Base):
    __tablename__ = 'miasto'

    id_miasto = Column(Numeric(8, 0), primary_key=True)
    miasto_nazwa = Column(String(150))
    id_wojewodztwo = Column(ForeignKey('wojewodztwo.id_wojewodztwo'))
    gps_latitude = Column(Numeric(15, 12))
    gps_longitude = Column(Numeric(15, 12))
    czy_prognoza = Column(Boolean, server_default=text("false"))

    wojewodztwo = relationship('Wojewodztwo')


class SocialaccountSocialtoken(Base):
    __tablename__ = 'socialaccount_socialtoken'
    __table_args__ = (
        UniqueConstraint('app_id', 'account_id'),
    )

    id = Column(Integer, primary_key=True, server_default=text("nextval('socialaccount_socialtoken_id_seq'::regclass)"))
    token = Column(Text, nullable=False)
    token_secret = Column(Text, nullable=False)
    expires_at = Column(DateTime(True))
    account_id = Column(ForeignKey('socialaccount_socialaccount.id', deferrable=True, initially='DEFERRED'), nullable=False, index=True)
    app_id = Column(ForeignKey('socialaccount_socialapp.id', deferrable=True, initially='DEFERRED'), nullable=False, index=True)

    account = relationship('SocialaccountSocialaccount')
    app = relationship('SocialaccountSocialapp')


class Obiekt(Base):
    __tablename__ = 'obiekt'

    id_obiekt = Column(Numeric(12, 0), primary_key=True)
    obiekt_nazwa = Column(String(100))
    obiekt_ulica_nr = Column(String(10))
    obiekt_kod_pocztowy = Column(CHAR(5))
    gps_latitude = Column(Numeric(15, 12))
    gps_longitude = Column(Numeric(15, 12))
    id_miasto = Column(ForeignKey('miasto.id_miasto'))
    id_jednostka = Column(ForeignKey('jednostka.id_jednostka'))
    temp_wew_proj = Column(Numeric(3, 1))
    obiekt_ulica = Column(String(150))

    jednostka = relationship('Jednostka')
    miasto = relationship('Miasto')


class PogodaHistoria(Base):
    __tablename__ = 'pogoda_historia'

    id_pogoda_h = Column(Numeric(20, 0), primary_key=True)
    temp_zewn_h = Column(Numeric(4, 2))
    wiatr_predkosc_h = Column(Numeric(7, 5))
    wiatr_kierunek_h = Column(Numeric(5, 2))
    zachmurzenie_h = Column(Numeric(5, 2))
    naslonecznienie_calk_h = Column(Numeric(6, 2))
    id_miasto = Column(ForeignKey('miasto.id_miasto'), nullable=False)
    czas_pogoda_h = Column(DateTime, nullable=False)
    naslonecznienie_rozpr_h = Column(Numeric(5, 2))
    naslonecznienie_bezpn_h = Column(Numeric(6, 2))
    naslonecznienie_szac_h = Column(Numeric(6, 2))
    wilgotnosc_wzgl_h = Column(Numeric(3, 0))
    temp_odczuw_h = Column(Numeric(4, 2))

    miasto = relationship('Miasto')


class PrognozaPogody(Base):
    __tablename__ = 'prognoza_pogody'

    id_prognoza_pogoda = Column(Numeric(20, 0), primary_key=True)
    czas_gen_prognoza = Column(DateTime, nullable=False)
    czy_biezaca = Column(Numeric(1, 0))
    id_miasto = Column(ForeignKey('miasto.id_miasto'))

    miasto = relationship('Miasto')


class InstalacjaModul(Base):
    __tablename__ = 'instalacja_modul'

    id_instalacja = Column(Numeric(9, 0), primary_key=True)
    id_modul = Column(ForeignKey('modul.id_modul'))
    id_obiekt = Column(ForeignKey('obiekt.id_obiekt'))
    data_od = Column(Date)
    data_do = Column(Date)
    biezaca_instalacja = Column(Boolean, server_default=text("true"))

    modul = relationship('Modul')
    obiekt = relationship('Obiekt')


class PrognozaPogodyDetale(Base):
    __tablename__ = 'prognoza_pogody_detale'

    id_prognoza_pogoda = Column(ForeignKey('prognoza_pogody.id_prognoza_pogoda'), nullable=False)
    czas_prognozy = Column(DateTime, nullable=False)
    temp_zewn_p = Column(Numeric(4, 2))
    wiatr_predkosc_p = Column(Numeric(7, 5))
    wiatr_kierunek_p = Column(Numeric(5, 2))
    naslonecznienie_calk_p = Column(Numeric(6, 2))
    zachmurzenie_p = Column(Numeric(5, 2))
    naslonecznienie_rozpr_p = Column(Numeric(5, 2))
    naslonecznienie_bezpn_p = Column(Numeric(6, 2))
    naslonecznienie_szac_p = Column(Numeric(6, 2))
    wilgotnosc_wzgl_p = Column(Numeric(3, 0))
    temp_odczuw_p = Column(Numeric(4, 2))
    id_prognoza_detale = Column(Numeric(25, 0), primary_key=True)

    prognoza_pogody = relationship('PrognozaPogody')


class KrzywaKorekt(Base):
    __tablename__ = 'krzywa_korekt'

    id_krzywa = Column(Numeric(9, 0), primary_key=True)
    krzywa_data_od = Column(Date)
    krzywa_data_do = Column(Date)
    czas_oblicz_krzywej = Column(DateTime(True))
    czy_biezaca = Column(Boolean)
    wsp_a = Column(Numeric(3, 2))
    wsp_b = Column(Numeric(3, 2))
    wsp_c = Column(Numeric(3, 2))
    wsp_d = Column(Numeric(3, 2))
    id_instalacja = Column(ForeignKey('instalacja_modul.id_instalacja'))
    h_wspstratciepla = Column(Numeric(4, 1))
    r2_wiatr = Column(Numeric(6, 5))
    r2_naslonecznienie = Column(Numeric(6, 5))

    instalacja_modul = relationship('InstalacjaModul')


class NastawyModul(Base):
    __tablename__ = 'nastawy_modul'

    id_nastawy = Column(Numeric(20, 0), primary_key=True)
    id_instalacja = Column(ForeignKey('instalacja_modul.id_instalacja'))
    czas_gen_nastaw = Column(DateTime(True))
    czas_start = Column(DateTime(True))
    status_nastawy = Column(CHAR(1))
    zrodlo_nastawy = Column(CHAR(1))
    czy_biezaca = Column(CHAR(1))

    instalacja_modul = relationship('InstalacjaModul')


class NastawyModDetale(NastawyModul):
    __tablename__ = 'nastawy_mod_detale'

    id_nastawy_mod_detale = Column(Numeric(20, 0))
    id_nastawy = Column(ForeignKey('nastawy_modul.id_nastawy'), primary_key=True)
    godzina_nastaw = Column(DateTime(True))
    temp_rown_zewn_nastaw = Column(Numeric(4, 1))


class OdczytModul(Base):
    __tablename__ = 'odczyt_modul'

    id_odczyt = Column(Numeric(30, 0), primary_key=True)
    id_instalacja = Column(ForeignKey('instalacja_modul.id_instalacja'))
    czas_odczytu = Column(DateTime(True))

    instalacja_modul = relationship('InstalacjaModul')


class ProfilCzasNastawModul(Base):
    __tablename__ = 'profil_czas_nastaw_modul'

    id_prof_czas_nast_mod = Column(Numeric(10, 0), primary_key=True)
    id_instalacja = Column(ForeignKey('instalacja_modul.id_instalacja'))
    data_od = Column(Date)
    data_do = Column(Date)
    id_profil_czas = Column(ForeignKey('profil_czas_nastaw.id_profil_czas'))

    instalacja_modul = relationship('InstalacjaModul')
    profil_czas_nastaw = relationship('ProfilCzasNastaw')


class ObnizeniaTempFinal(Base):
    __tablename__ = 'obnizenia_temp_final'

    id_obnizenia_temp_final = Column(Numeric(25, 0), primary_key=True)
    id_nastawy = Column(ForeignKey('nastawy_modul.id_nastawy'), unique=True)
    obniz_noc_od = Column(Date)
    obniz_noc_do = Column(Date)
    obniz_noc_temp = Column(Numeric(2, 0))
    obniz_dzien_od = Column(Date)
    obniz_dzien_do = Column(Date)
    obniz_dzien_temp = Column(Numeric(2, 0))

    nastawy_modul = relationship('NastawyModul', uselist=False)


class OdczytModulDetale(Base):
    __tablename__ = 'odczyt_modul_detale'

    id_odczyt_detale = Column(Numeric(35, 0), primary_key=True)
    id_odczyt = Column(ForeignKey('odczyt_modul.id_odczyt', ondelete='CASCADE'))
    temp_zasilania_odczyt = Column(Numeric(5, 1))
    temp_powrot_odczyt = Column(Numeric(5, 1))
    temp_zewn_odczyt = Column(Numeric(5, 1))
    przeplyw_odczyt = Column(Numeric(8, 2))
    moc_dostarczona_odczyt = Column(Numeric(8, 2))
    zuzycie_ciepla_odczyt = Column(Numeric(8, 1))
    czas_odczytu = Column(DateTime(True))

    odczyt_modul = relationship('OdczytModul')
