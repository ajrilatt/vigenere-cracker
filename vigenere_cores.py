# Adam Rilatt
# 90 / 09 / 20
# Multi-core Vigenere Cracker

import multiprocessing
import itertools

ALPHABET = 'abcdefghijklmnopqrstuvwxyz'
LOWER_BOUND = 0
UPPER_BOUND = 10
CHI_THRESHOLD = 35
english = [
    0.08167, 0.01492 ,0.02782, 0.04253, 0.12702, 0.02228, 0.02015,
    0.06094, 0.06966, 0.00153, 0.00772, 0.04025, 0.02406, 0.06749,
    0.07507, 0.01929, 0.00095, 0.05987, 0.06327, 0.09056, 0.02758,
    0.00978, 0.02360, 0.00150, 0.01974, 0.00074
]


def chi2(text, threshold = CHI_THRESHOLD):

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


def worker(return_dict, ciphertext, subset, depth):

    name = multiprocessing.current_process().name
    best = 9999
    best_key = ''

    for subchar in subset:
        for test_key in permute_strings(depth):

            test_key = subchar + test_key

            chi_passed, chi = chi2(devigenere(ciphertext, test_key))
            if chi < best:
                best     = chi
                best_key = test_key

    return_dict[name] = (best_key, best)


def crack(text):

    manager = multiprocessing.Manager()
    return_dict = manager.dict()

    subsets = [
        'ab', 'cd', 'ef', 'gh', 'ij', 'kl', 'mn', 'op', 'qr', 'st', 'uvw', 'xyz'
    ]

    for depth in range(LOWER_BOUND, UPPER_BOUND):

        print("\nChecking passwords of length %d..." % (depth + 1))

        jobs = []
        for i in range(12):
            p = multiprocessing.Process(target = worker, args = (
                                        return_dict, text, subsets[i], depth
                                        ))
            jobs.append(p)
            p.start()

        for proc in jobs:
            proc.join()

        key, best = max(return_dict.values())
        print("%s => %f" % (key, best))

        if best < CHI_THRESHOLD:
            return key

if __name__ == '__main__':

    s = '''The Purdue article also cautions that even if our dogs aren’t eating grass because they’re trying to vomit, care should be taken to make sure they’re not sick: “Your veterinarian can determine whether your dog has an underlying gastrointestinal disease with a physical exam, fecal exam, and blood tests including a blood count and chemistry panel. The blood count tells us if there is inflammation or blood loss that could indicate bleeding into the GI tract; the chemistry panel assesses the health and function of body systems including the pancreas and liver, which are intricately associated with the gastrointestinal tract. If your veterinarian diagnoses GI disease, proper treatment can be prescribed. So when should you call your veterinarian? If your pet experiences lethargy, diarrhea, weight loss concurrent with grass-induced vomiting, she should see the vet. If not, you can probably rest easy knowing that your dog is just doing what dogs do.”'''

    cipher = '''WVKVSURAKYUHOIJHORYMFOAZGRBYZFDHKBCQWLUSURUMQDFKTRHOZOLJUXGQVPKIYXGKZFHMXKRUMOTEWCBUKLHIGPHGNUSORHKRDYKTRRAGQCVIXKRKSEXCQCZYGFYEUSUJKZCUWTGPLOTIYQRKZCUAOTCZVKZFHFEUSURUMFDGGTSQRKXJBWTMEDGZXMLBZKQWWTGJGWYKYVSCORKOVNWVWIGJHLGSDHQGRCAOSGLGPRUMGHKYRVWTIJXROTEDPRUMGQUALWOTJAKSSOQWFEVYQSRZFHPRUMGQUALWHKRJVIYODWVKXCLGOTDOOSSYWWUTMUPRUMGZUYQWVGZARIRJGQROIYWSHRCHROTELBZURKSMORUOIZRKSINCPWYZPBDGTCOOYYCVGKYRKSNKYOHNGLGTATAWWUTMIPUJWVMYZCPGOTAOIJOLJHNKNDBIXCDGGTBOWBKPZVOIFDFKOLWFOIYWSREYVGUIGDHKJULHNZFHUGYRUCOTRHGZOLDZZXYFHOLWRIXBCWSXOLDFOGLGWGMLRGKYELROYCDGKVPRDKXRUSGZKHBZIYQPKVPHGIXGESJYMZVKTQKCARBBCAIYOZEUSUJKZCUWTGPLOTODBCAXNHHKDNHFOKLFSYRCWVGXEBROGPUVKGUHWMNROCYYARBIAPUSTZULHNMPDGYOLGIIKBYCSORLBMYFHGNUSORYKCWVKBCWWLTMWMUAADBVXMEOHRWUSYZCDGEQLRKOTEWVGZWRIXJMJWYPSVHJUGQUCNYWRUMQGC'''

    # should be doggy or doggie or something like that
    found_key = crack(cipher)
    print(devigenere(cipher, found_key))
