from MainApps.models import ShippingCharge, Website, PcPeripheralCart,PcPheripherals
import json

def website_info(request):

    PROVINCES = [
        {
            "name": "Koshi Province",
            "districts": {
                "Bhojpur": ["Bhojpur Municipality", "Shadananda", "Pauwadungma"],
                "Dhankuta": ["Dhankuta Municipality", "Chhathar", "Shahidbhumi"],
                "Ilam": ["Ilam Municipality", "Maijogmai", "Fikkal"],
                "Jhapa": ["Birtamode", "Mechinagar", "Kankai"],
                "Khotang": ["Diktel", "Sakela", "Khotehang"],
                "Morang": ["Biratnagar", "Rangeli", "Letang"],
                "Okhaldhunga": ["Okhaldhunga Municipality", "Siddhicharan", "Khijidemba"],
                "Panchthar": ["Phidim", "Yangnam", "Maimajhuwa"],
                "Sankhuwasabha": ["Khandbari", "Chichila", "Madi"],
                "Solukhumbu": ["Salleri", "Chheplung", "Beni"],
                "Sunsari": ["Inaruwa", "Duhabi", "Itahari"],
                "Taplejung": ["Taplejung Municipality", "Phungling", "Sidingwa"],
                "Terhathum": ["Myanglung", "Aathrai", "Madi"],
                "Udayapur": ["Gaighat", "Katari", "Triyuga"]
            }
        },
        {
            "name": "Madhesh Province",
            "districts": {
                "Bara": ["Kalaiya", "Pheta", "Bishrampur"],
                "Dhanusha": ["Janakpur", "Mithila Bihari", "Shivajee"],
                "Mahottari": ["Jaleshwar", "Bardibas", "Gaushala"],
                "Parsa": ["Birgunj", "Bharatpur", "Parwanipur"],
                "Rautahat": ["Gaur", "Chandranigahapur", "Bairgania"],
                "Saptari": ["Rajbiraj", "Kanchanrup", "Shambhunath"],
                "Sarlahi": ["Malangawa", "Barahathwa", "Sauraha"],
                "Siraha": ["Siraha Municipality", "Lahan", "Golbazar"]
            }
        },
        {
            "name": "Bagmati Province",
            "districts": {
                "Bagmati": ["Kathmandu", "Lalitpur", "Bhaktapur"],
                "Chitwan": ["Bharatpur", "Khairahani", "Madi"],
                "Dhading": ["Dhading Besi", "Benighat", "Netrawati"],
                "Dolakha": ["Bhimeshwar", "Jiri", "Kshetrapa"],
                "Kabhrepalanchok": ["Dhulikhel", "Banepa", "Panauti"],
                "Makwanpur": ["Hetauda", "Thaha", "Bakaiya"],
                "Nuwakot": ["Bidur", "Trishuli", "Belkot"],
                "Ramechhap": ["Manthali", "Okhaldhunga", "Sunapati"],
                "Rasuwa": ["Dhunche", "Briddim", "Gosaikunda"],
                "Sindhupalchok": ["Chautara", "Jugal", "Melamchi"]
            }
        },
        {
            "name": "Gandaki Province",
            "districts": {
                "Baglung": ["Baglung Municipality", "Dhorpatan", "Nisi"],
                "Gorkha": ["Gorkha Municipality", "Palungtar", "Siddhartha"],
                "Kaski": ["Pokhara", "Lekhnath", "Pardi"],
                "Lamjung": ["Besisahar", "Dharche", "Sundarbazar"],
                "Manang": ["Chame", "Nar", "Besisahar"],
                "Mustang": ["Jomsom", "Lo Manthang", "Kagbeni"],
                "Myagdi": ["Beni", "Dhaulagiri", "Beni Municipality"],
                "Parbat": ["Kusma", "Khopasi", "Dhorpatan"],
                "Syangja": ["Putalibazar", "Chandrakot", "Waling"],
                "Tanahun": ["Damauli", "Bhanu", "Byas"]
            }
        },
        {
            "name": "Lumbini Province",
            "districts": {
                "Banke": ["Nepalgunj", "Khajura", "Duduwa"],
                "Bardiya": ["Gulariya", "Thakurbaba", "Bansgadhi"],
                "Dang": ["Ghorahi", "Tulsipur", "Lamahi"],
                "Kapilvastu": ["Taulihawa", "Shivaraj", "Suddhodhan"],
                "Palpa": ["Tansen", "Rani Mahal", "Siddhartha"],
                "Rupandehi": ["Siddharthanagar", "Butwal", "Bhairahawa"],
                "Pyuthan": ["Pyuthan", "Swargadwari", "Bhalubang"],
                "Rolpa": ["Liwang", "Thawang", "Runtigadhi"],
                "Rukum West": ["Musikot", "Bheri", "Chaurjahari"],
                "Salyan": ["Salyan", "Kamalbazar", "Chhatreshwori"]
            }
        },
        {
            "name": "Karnali Province",
            "districts": {
                "Dailekh": ["Dailekh", "Narayan", "Khalanga"],
                "Dolpa": ["Dunai", "Juphal", "Sankhuwasabha"],
                "Humla": ["Simikot", "Chankheli", "Sarkegad"],
                "Jumla": ["Jumla", "Tila", "Sinja"],
                "Kalikot": ["Manma", "Sanni Triveni", "Khandachakra"],
                "Mugu": ["Gamgadhi", "Chhayanath", "Mugu Municipality"],
                "Surkhet": ["Birendranagar", "Bheriganga", "Barahatal"],
                "Jajarkot": ["Jajarkot", "Khalanga", "Chhedagad"]
            }
        },
        {
            "name": "Sudurpashchim Province",
            "districts": {
                "Baitadi": ["Baitadi", "Dogada", "Dilli Bazar"],
                "Dadeldhura": ["Dadeldhura", "Amargadhi", "Parshuram"],
                "Darchula": ["Darchula", "Mahakali", "Byas"],
                "Doti": ["Dipayal Silgadhi", "Purbichauki", "Jorayal"],
                "Kailali": ["Dhangadhi", "Godawari", "Tikapur"],
                "Kanchanpur": ["Mahendranagar", "Shuklaphanta", "Bhimdatta"]
            }
        }
    ]

    website = Website.objects.first()

    if request.user.is_authenticated:
        pc_cart = PcPeripheralCart.objects.filter(user=request.user)
        total_cart_amount = sum(float(item.total_cost) for item in pc_cart)
        total_cart_count = sum(item.quantity for item in pc_cart)  # total items in cart
    else:
        pc_cart = []
        total_cart_amount = 0.0
        total_cart_count = 0

    return {
        'website': website,
        'pc_cart': pc_cart,
        'inspir': PcPheripherals.objects.order_by('?')[:5],
        'total_cart_amount': total_cart_amount,
        'total_cart_count': total_cart_count,  # new key for templates
        'provinces': PROVINCES,
        'provinces_json': json.dumps(PROVINCES),  # useful for JS
        'shipping_charges': ShippingCharge.objects.all()
    }



