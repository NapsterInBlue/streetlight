all_clean = [
    'everything went numb',
    "that'll be the day",
    'point / counterpoint',
    'if and when we rise again',
    'a better place, a better time',
    'we are the few',
    'failing, flailing',
    "here's to life",
    'a moment of silence',
    'a moment of violence',
    'the saddest song',
    'the big sleep',

    'dear sergio',
    'sick and sad',
    'keasbey nights',
    'day in, day out',
    'walking away',
    'giving up, giving in',
    'on & on & on',
    'riding the fourth wave',
    'this one goes out to...',
    'supernothing',
    '9mm and a three piece suit',
    "kristina she don't know i exist",
    'as the footsteps die out forever',
    '1234 1234',
    
    'we will fall together',
    "down, down, down to mephisto's cafe",
    'would you be impressed?',
    'one foot on the gas, one foot in the grave',
    'watch it crash',
    'somewhere in the between',
    'forty days',
    'the blonde lead the blind',
    'the receiving end of it all',
    'what a wicked gang are we',
    
    'birds flying away',
    'hell',
    'just',
    'skyscraper',
    'punk rock girl',
    'linoleum',
    'me and julio down by the schoolyard',
    'they provide the paint',
    'red rubber ball',
    'the troubadour',
    'such great heights',

    'the three of us',
    'ungrateful',
    'the littlest things',
    'the hands that thieve',
    'with any sort of certainty',
    'if only for memories',
    'they broke him down',
    'toe to toe',
    'oh me, oh my',
    'your day will come'
    ]


all_possible = dict.fromkeys(all_clean, 0)


def build_setlist_dict(setlist_):
    setlist = set([x.lower() for x in setlist_])
    set_dict = all_possible.copy()

    for song in setlist:
        if set_dict.get(song) is not None:
            set_dict[song] = 1

    trial = ['1234 1234', '1234, 1234']
    if set(trial).intersection(setlist):
        set_dict['1234 1234'] = 1

    trial = 'day in day out'
    if trial in setlist:
        set_dict['day in, day out'] = 1

    trial = set(['point / keasbey nights / counterpoint',
                 'point/counterpoint',
                 'point/counterpoint / keasbey nights'])
    if trial.intersection(setlist):
        set_dict['point / counterpoint'] = 1

    trial = set(['point / keasbey nights / counterpoint',
                 'point/counterpoint / keasbey nights'])
    if trial.intersection(setlist):
        set_dict['keasbey nights'] = 1

    trial = set(['they provide the paint for the picture perfect masterpiece that you will paint on the corners of your eyelids',
                 'they provide the paint for the picture perfect masterpiece that you will paint on the insides of your eyelids'])
    if trial.intersection(setlist):
        set_dict['they provide the paint'] = 1

    trial = 'what a wicked gang are we below'
    if trial in setlist:
        set_dict['what a wicked gang are we'] = 1

    return set_dict