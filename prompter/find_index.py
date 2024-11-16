import re

def find_substring_indices(text, substring):
    """Finds the start and end indices of the first occurrence of a substring within a string.

    Args:
        text (str): The main string to search.
        substring (str): The substring to find.

    Returns:
        tuple: A tuple containing the start and end index (inclusive) of the substring, or None if not found.
    """
    match = re.search(re.escape(substring), text)  # Use re.escape to handle special characters in the substring
    
    if match:
        start_index = match.start()
        end_index = match.end()  # Subtract 1 to make it inclusive
        return start_index, end_index
    else:
        return None

# Example usage
# text = "Ang mga biyahe sa barko paingon sa Bohol, Camotes, Leyte, Negros, Siquijor gipasuspenso, pahibawo sa Coast Guard District Central Visayas. Daghang biyahe sa barko nga gikan sa Cebu ang gipasuspenso tungod sa daotang panahon ug dagkong bawod. Ang Coast Guard District Central Visayas nagmando sa paghunong sa pagbiyahe tungod sa bagyong Ferdie (Bebinca), Sabado, Sept. 14, 2024. Mabalik sa normal nga operasyon kon molurang ang dautang panahon. Nagpagawas og travel advisory para sa mga barko nga adunay gross tonnage nga 250 ug ubos, nga nakaapekto sa mga rota gikan sa Negros Oriental, Kasadpang Bohol, Sidlangan Bohol, Camotes, ug Siquijor. Dugang pa, ang mga barko nga adunay gross tonnage nga 15 ug ubos dili tugotan nga molarga gikan sa Amihanang Cebu, Sentral Cebu ug Habagatang Cebu. Ang Cebu Port Authority (CPA) mipahibalo pinaagi sa ilang Facebook page mahitungod sa mga kanseladong biyahe gikan sa Cebu padulong sa Bohol. Si CPA public information officer Mary Balaba Balagtas-Balaguer, sa iyang chat message sa SunStar Cebu, nitambag sa mga pasahero angayan nga mopauli lang una ug magpaabot sa mga bag-ong update. “Mga stranded passengers mao na among i-turn over to concerned LGU (local government unit) aron moagi og shelter kay bawal magtambay ang mga stranded passengers sa pantalan, labi na kusog ang hangin ug balod,” matod pa ni Balagtas-Balaguer. / JPS, PNA"
# text = "Daghang biyahe sa barko nga gikan sa Cebu ang gipasuspenso tungod sa daotang panahon ug dagkong bawod."
# substring = "daotang panahon ug dagkong bawod."

# text = "Ang Coast Guard District Central Visayas nagmando sa paghunong sa pagbiyahe tungod sa bagyong Ferdie (Bebinca), Sabado, Sept. 14, 2024."
# substring = "bagyong Ferdie"
# text = "Anaa na sa Regional Holding Admin Unit sa Police Regional Office (PRO) 7 ang hepe sa Marigondon Police Station lakip na ang duha ka personnel nga giingong nangulata sa usa ka tinun-an human dudahi nga nangawat sa iyang amo sa miaging semana. Matod ni Police Lieutenant Colonel Lennon Marjo Abacay, spokesperson ni Police Brigadier General Jorge Abad hepe sa kapulisan sa Central Visayas nga kabahin sa proseso ang pagrelibo sa mga polis kon adunay himuon nga imbestigasyon batok kanila. Iyang gipasabot nga aron dili makaempluwensya sa himuon nga imbestigasyon kinahanglan sila nga parelibohan sa katungdanan. Gipasalig ni Abacay nga ang hepe sa PRO-7 dili modupa sa mga polis kon mapamatud-an nga sad-an sa ilang nahimo. “Klaro man ang position sa atong Regional Director Police Brigadier General Jorge Abad sa ingon ani nga mga sitwasyon, we will never condone any deviations from the police operational procedure, kung naa man gani tay mapamatud-an nga ni violate sa police operational procedure in the conduct of investigation as in this case then we will file the necessary charges,” matod ni Abacay. Apan mipasabot si Abacay nga ilang hatagan og oportunidad ang matag personnel nga makapresentar sa ilang kaugalingon kung unsa ka tinuod ang pangangkon sa reklamante nga kabahin sa due process. Una na nga mipahinumdom ang pangulo sa PRO 7 atol sa iyang paglingkod nga sa iyang katungdanan sa tanang polis nga kinahanglang mobalik gyud sila sa basic sa pagpamulis. Kinahanglan nga sundon ang unsay nalatid sa police operational procedure ug kung dunay molapas niini mibahad ang heneral nga iyang silotan kutob sa ilang mahimo pinaagi sa pagpasaka sa kaso. / AYB"
# # substring = "Siyang gipasabot nga ang pagrelibo sa mga polis kabahin sa proseso kon adunay himuon nga imbestigasyon."
# # substring = "pagrelibo sa mga polis"
# substring = "Apan mipasabot si Abacay nga ilang hatagan og oportunidad ang matag personnel nga makapresentar sa ilang kaugalingon kung unsa ka tinuod ang pangangkon sa reklamante nga kabahin sa due process."

text = "Samdan sa iyang wala nga bahin sa ilok ang 43 anyos, nga habal-habal drayber sa dihang gidunggab sa iyang gisingil sa utang niadtong alas 6:16 sa gabii, Martes, Oktubre 8, 2024. Ang insedente nahitabo sa Purok Avocado, Sitio Ylaya, lungsod sa Liloan, Cebu. Samtang misibat ang 20 anyos nga suspek nga gitago sa pangala’ng Martinito, usa usab ka habal-habal drayber nga silingan sa biktima. Si Police Chief Master Sgt. Arne Goc-ong, imbestigador sa Liloan Police Station mibutyag sa pakighinabi sa Superbalita Cebu nga nagkalalis ang biktima ug suspek. Nasayran nga ang asawa sa suspek nakautang og P1,000 ngadto sa biktima nga gisigehan og panangil apan giingong gahi mobayad ang maong utangan. Sulod sa makatulo ka higayon nga gipaningil sa biktima ang magtiayon nga nakautang niya, human nga iyang nasayran nga mihatag og pang down payment ang suspek sa ilang giutang nga motorsiklo. “Nagtuo ang biktima nga duna nay kwarta kay naka-down gud sa bag-ong motor. Mao nga iyang gibalikbalikan sa pagpaningil,” matod pa ni PCMS Goc-ong. Apan wala gihapon mobayad ang suspek ug asawa niini. Nianang gabii gitawag ang biktima ni alyas Martinito sa dihang gikamay niya ang biktima nga paduolon. Gibati og ka-excited ang biktima sa pagtuo nga mabayran na siya sa maong utang hinungdan nga nagdalidali sa pagduol. Apan nahitabo na hinuon ang mainitong panaglalis ug way bayad nga nakuha ang biktima. Gamit ang kitchen si alyas Martinito mihana og duslak ngadto sa biktima apan wa kini ma-intimano sa dihang giwakli ra sab sa asawa sa suspek ang kamot niini og didto miigo ang kutsilyo sa ilok sa biktima. Gitabang ang biktima pinaagi sa pagdala sa Danao City District Hospital aron nga magpaalim sa iyang samad, samtang dali nga misibat ang suspek. Si Goc-ong miingon nga nagpaabot sila sa suspek human mipahibalo ang kabanay nga mo-surrender. Giandam na sab nila ang kasong frustrated murder batok sa suspek. / GPL "
substring = "Ang insedente nahitabo sa Purok Avocado, Sitio Ylaya, lungsod sa Liloan, Cebu."

indices = find_substring_indices(text, substring)
if indices:
    print(f"Substring '{substring}' found from index {indices[0]} to {indices[1]}")
    print(text[indices[0]:indices[1]])
else:
    print("Substring not found")

