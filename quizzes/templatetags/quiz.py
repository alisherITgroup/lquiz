from django.template import Library

register = Library()

@register.filter
def results(cases):
    html = ""
    counter = 1
    for case in cases:
        if cases[case]['status'] == "Accepted":
            acc = f"""
    <a href="#" class="block p-6 bg-white border border-gray-200 rounded-lg shadow hover:bg-gray-100 dark:bg-gray-800 dark:border-gray-700 dark:hover:bg-gray-700">
        <h5 class="mb-2 text-2xl font-bold tracking-tight text-gray-900 dark:text-white">{counter}. {cases[case]['question']}</h5>
        <p class="font-normal text-gray-700 dark:text-gray-400">Correct answer: {cases[case]['correct']}</p>
        <p class="font-normal text-gray-700 dark:text-gray-400">Your answer: {cases[case]['answer']}</p>
        <p class="text-green-500">Accepted</p>
    </a> <br>

        """
        else:
            acc = f"""
    <a href="#" class="block p-6 bg-white border border-gray-200 rounded-lg shadow hover:bg-gray-100 dark:bg-gray-800 dark:border-gray-700 dark:hover:bg-gray-700">
        <h5 class="mb-2 text-2xl font-bold tracking-tight text-gray-900 dark:text-white">{cases[case]['question']}</h5>
        <p class="font-normal text-gray-700 dark:text-gray-400">{cases[case]['correct']}</p>
        <p class="font-normal text-gray-700 dark:text-gray-400">{cases[case]['answer']}</p>
        <p class="text-red-500">Wrong</p>
    </a> <br>

        """
        html += acc
        counter += 1
    return html