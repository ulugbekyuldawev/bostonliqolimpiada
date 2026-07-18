from django.core.management.base import BaseCommand
from django.db import transaction

from olympiad.models import Subject, Level, Question


PYTHON_2_SINF_QUESTIONS = [
    ('Python nima?', 'Dasturlash tili', 'Ovqat turi', 'Hayvon turi', 'Davlat nomi', 'A'),
    ('Python tilida ekranga matn chiqarish uchun qaysi buyruq ishlatiladi?', 'print()', 'input()', 'echo()', 'write()', 'A'),
    ('print("Salom") buyrug\'i ekranga nimani chiqaradi?', 'Salom', '"Salom"', 'print', 'Xato beradi', 'A'),
    ('Python tilida foydalanuvchidan ma\'lumot olish uchun qaysi buyruq ishlatiladi?', 'print()', 'input()', 'get()', 'read()', 'B'),
    ('2 + 3 amalining natijasi nechchiga teng?', '5', '6', '23', '1', 'A'),
    ('10 - 4 amalining natijasi nechchiga teng?', '4', '6', '14', '40', 'B'),
    ('Python tilida son bilan matnni bir-biridan ajratish uchun nimadan foydalaniladi?', 'Qavs', 'Qo\'shtirnoq', 'Nuqta', 'Vergul', 'B'),
    ('x = 5 buyrug\'i nimani anglatadi?', 'x sonini 5 ga taqqoslaydi', 'x nomli o\'zgaruvchiga 5 qiymatini beradi', '5 ni chop etadi', 'Xato buyruq', 'B'),
    ('Python tilida izoh (comment) yozish uchun qaysi belgidan foydalaniladi?', '//', '#', '**', '&&', 'B'),
    ('3 * 4 amalining natijasi nechchiga teng?', '7', '12', '34', '1', 'B'),
    ('Python dasturlash tilini kim yaratgan?', 'Bill Gates', 'Guido van Rossum', 'Steve Jobs', 'Mark Zuckerberg', 'B'),
    ('Quyidagilardan qaysi biri Python o\'zgaruvchisi nomi bo\'lishi mumkin emas?', 'son1', '_son', '1son', 'sonBir', 'C'),
    ('Python tilida "va" mantiqiy amalini bildiruvchi kalit so\'z qaysi?', 'or', 'and', 'not', 'if', 'B'),
    ('Python tilida "yoki" mantiqiy amalini bildiruvchi kalit so\'z qaysi?', 'or', 'and', 'not', 'if', 'A'),
    ('for tsikli nima uchun ishlatiladi?', 'Shartni tekshirish uchun', 'Amalni bir necha marta takrorlash uchun', 'Xato chiqarish uchun', 'Fayl ochish uchun', 'B'),
    ('if buyrug\'i nima uchun ishlatiladi?', 'Shartni tekshirish uchun', 'Sonlarni qo\'shish uchun', 'Ro\'yxat yaratish uchun', 'Matn chiqarish uchun', 'A'),
    ('[1, 2, 3] Python tilida qanday ma\'lumot turi hisoblanadi?', 'Son', 'Matn', 'Ro\'yxat (list)', 'Mantiqiy qiymat', 'C'),
    ('Python tilida matn (satr) qanday belgilar orasiga yoziladi?', 'Qavslar ()', 'Qo\'shtirnoq " " yoki \' \'', 'Katakcha { }', 'Kvadrat qavs [ ]', 'B'),
    ('len("Salom") natijasi nechchiga teng?', '4', '5', '6', 'Xato', 'B'),
    ('True va False Python tilida qanday ma\'lumot turiga tegishli?', 'Son', 'Matn', 'Mantiqiy (bool)', 'Ro\'yxat', 'C'),
    ('5 == 5 ifodasining natijasi nima bo\'ladi?', 'True', 'False', '5', 'Xato', 'A'),
    ('5 > 3 ifodasining natijasi nima bo\'ladi?', 'True', 'False', '8', 'Xato', 'A'),
    ('Python faylining kengaytmasi (nomi oxiri) qanday bo\'ladi?', '.py', '.exe', '.txt', '.doc', 'A'),
    ('print(2 + 2) buyrug\'i ekranga nimani chiqaradi?', '2+2', '4', '22', 'Xato', 'B'),
    ('Python tilida bitta qatorda bir nechta buyruq yozish uchun odatda nima ishlatiladi?', 'Vergul', 'Nuqta-vergul (;)', 'Ikki nuqta (:)', 'Amperson (&)', 'B'),
    ('while tsikli qachon to\'xtaydi?', 'Hech qachon to\'xtamaydi', 'Shart yolg\'on (False) bo\'lganda', 'Dastur boshlanganda', 'Ekran tozalanganda', 'B'),
    ('Python tilida ro\'yxatning birinchi elementi qanday raqamdan boshlanadi?', '1', '0', '-1', '10', 'B'),
    ('def kalit so\'zi Python tilida nima uchun ishlatiladi?', 'Funksiya yaratish uchun', 'Ro\'yxat yaratish uchun', 'Fayl o\'chirish uchun', 'Dasturni to\'xtatish uchun', 'A'),
    ('Python interpretatsiyalanuvchi (interpreted) til hisoblanadimi?', 'Ha', 'Yo\'q', 'Faqat Windows\'da', 'Faqat Mac\'da', 'A'),
    ('IDLE nima?', 'Python dasturlarini yozish va ishga tushirish uchun dastur', 'Internet brauzeri', 'Musiqa pleyeri', 'Video tahrirlash dasturi', 'A'),
]


class Command(BaseCommand):
    help = 'IT fani uchun 2-sinf darajasini va Python fanidan 30 ta boshlang\'ich testni bazaga qo\'shadi.'

    @transaction.atomic
    def handle(self, *args, **options):
        subject, _ = Subject.objects.get_or_create(name='IT')

        level, level_created = Level.objects.get_or_create(
            subject=subject,
            name='2-sinf',
            defaults={'duration_minutes': 30},
        )
        if level_created:
            self.stdout.write(self.style.SUCCESS(f"Yaratildi: {subject.name} - {level.name}"))
        else:
            self.stdout.write(self.style.WARNING(f"Allaqachon mavjud: {subject.name} - {level.name}"))

        existing_count = Question.objects.filter(subject=subject, level=level).count()
        if existing_count:
            self.stdout.write(self.style.WARNING(
                f"Diqqat: bu daraja uchun allaqachon {existing_count} ta savol bor. "
                f"Yangi 30 ta savol shularning ustiga qo'shiladi."
            ))

        created_count = 0
        for text, a, b, c, d, correct in PYTHON_2_SINF_QUESTIONS:
            Question.objects.create(
                subject=subject,
                level=level,
                text=text,
                option_a=a,
                option_b=b,
                option_c=c,
                option_d=d,
                correct_answer=correct,
            )
            created_count += 1

        self.stdout.write(self.style.SUCCESS(
            f"Tayyor! IT / 2-sinf uchun {created_count} ta Python savoli qo'shildi."
        ))
