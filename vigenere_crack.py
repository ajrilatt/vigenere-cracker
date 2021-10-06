# Adam Rilatt
# 09 / 07 / 20
# Vigenere Cracker

import itertools

ALPHABET = 'abcdefghijklmnopqrstuvwxyz'
HARD_CAP = 12
english = [
    0.08167, 0.01492 ,0.02782, 0.04253, 0.12702, 0.02228, 0.02015,
    0.06094, 0.06966, 0.00153, 0.00772, 0.04025, 0.02406, 0.06749,
    0.07507, 0.01929, 0.00095, 0.05987, 0.06327, 0.09056, 0.02758,
    0.00978, 0.02360, 0.00150, 0.01974, 0.00074
]

def chi2(text, threshold = 35):

    ''' We compare the count of letters in a potentially deciphered text
        to the standard English distribution. If it's below the threshold,
        we say it's most likely English.                                     '''

    counts = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    total  = 0
    chi2   = 0

    for i, char in enumerate(ALPHABET):
        c = text.count(char)
        counts[i] += c
        total += c

    for i in range(26):
        chi2 += ((counts[i] - total * english[i]) ** 2) / (total * english[i])

    return (True if chi2 <= threshold else False, chi2)


def devigenere(ciphertext, key):
    plaintext = []
    append = plaintext.append
    ciphertext = map(str.lower, ciphertext)
    for i, letter in enumerate(ciphertext):
        x = 97 + (ord(letter) - ord(key[i % len(key)]) + 26) % 26
        append(chr(x))
    return ''.join(plaintext)


def permute_strings(n):
    for p in itertools.product(ALPHABET, repeat = n):
        yield ''.join(p)

def test(ciphertext, start = 1):

    best = 9999

    for length in range(start, HARD_CAP):

        print('\nTesting key length %d...' % length)

        for test_key in permute_strings(length):

            chi_passed, chi = chi2(devigenere(ciphertext, test_key))
            if chi < best:
                best = chi
            print('%s => %f (best %f)' % (test_key, chi, best), end='\r')
            if chi_passed:
                return test_key





if __name__ == '__main__':

    s = '''The Purdue article also cautions that even if our dogs aren’t eating grass because they’re trying to vomit, care should be taken to make sure they’re not sick: “Your veterinarian can determine whether your dog has an underlying gastrointestinal disease with a physical exam, fecal exam, and blood tests including a blood count and chemistry panel. The blood count tells us if there is inflammation or blood loss that could indicate bleeding into the GI tract; the chemistry panel assesses the health and function of body systems including the pancreas and liver, which are intricately associated with the gastrointestinal tract. If your veterinarian diagnoses GI disease, proper treatment can be prescribed. So when should you call your veterinarian? If your pet experiences lethargy, diarrhea, weight loss concurrent with grass-induced vomiting, she should see the vet. If not, you can probably rest easy knowing that your dog is just doing what dogs do.”'''

    cipher = '''WVKVSURAKYUHOIJHORYMFOAZGRBYZFDHKBCQWLUSURUMQDFKTRHOZOLJUXGQVPKIYXGKZFHMXKRUMOTEWCBUKLHIGPHGNUSORHKRDYKTRRAGQCVIXKRKSEXCQCZYGFYEUSUJKZCUWTGPLOTIYQRKZCUAOTCZVKZFHFEUSURUMFDGGTSQRKXJBWTMEDGZXMLBZKQWWTGJGWYKYVSCORKOVNWVWIGJHLGSDHQGRCAOSGLGPRUMGHKYRVWTIJXROTEDPRUMGQUALWOTJAKSSOQWFEVYQSRZFHPRUMGQUALWHKRJVIYODWVKXCLGOTDOOSSYWWUTMUPRUMGZUYQWVGZARIRJGQROIYWSHRCHROTELBZURKSMORUOIZRKSINCPWYZPBDGTCOOYYCVGKYRKSNKYOHNGLGTATAWWUTMIPUJWVMYZCPGOTAOIJOLJHNKNDBIXCDGGTBOWBKPZVOIFDFKOLWFOIYWSREYVGUIGDHKJULHNZFHUGYRUCOTRHGZOLDZZXYFHOLWRIXBCWSXOLDFOGLGWGMLRGKYELROYCDGKVPRDKXRUSGZKHBZIYQPKVPHGIXGESJYMZVKTQKCARBBCAIYOZEUSUJKZCUWTGPLOTODBCAXNHHKDNHFOKLFSYRCWVGXEBROGPUVKGUHWMNROCYYARBIAPUSTZULHNMPDGYOLGIIKBYCSORLBMYFHGNUSORYKCWVKBCWWLTMWMUAADBVXMEOHRWUSYZCDGEQLRKOTEWVGZWRIXJMJWYPSVHJUGQUCNYWRUMQGC'''

    print(chi2(s))

    #print(devigenere('HYESUPZFWVTKWJAGKWHFFGNIRVCEETHZNTYCGKEZOLOMEQKZSCOCKH', 'orange'))
    found_key = test(cipher)
    print(devigenere(cipher, found_key))
