from services.UserService import UserService


class InterestService:
    interests = {
        'Sport': ['Football', 'Rugby', 'Soccer', 'Basketball'],
        'Books': ['Dystopia', 'Romance', 'Fantasy', 'Non Fiction', 'Thriller', 'Crime'],
        'Films': ['Comedy', 'Thriller', 'Action', 'Sport', 'Indie', 'Horror'],
        'Music': ['Indie', 'Heavy Metal', 'Rock', 'Pop', 'Hip Hop', 'Rap', 'Electronic'],
        'Entertainment': ['Theater', 'Concerts', 'Board Games', 'Video Games', 'Tabletop'],
        'Others': ['Volunteering', 'Memes', 'Travelling', 'Sleeping']
    }

    @staticmethod
    def events_by_interests_filter_builder(user_id):
        def intersection(list1, list2):
            return [element for element in list1 if element in list2]

        def interests_in_event(event):
            event_interests = [interest.label for user in event.users for interest in user.interests]
            event_interests = list(set(event_interests))  # Removing duplicates

            return event_interests

        user_interests = [interest.label for interest in UserService.get_user_by_id(user_id).interests]

        return lambda event: intersection(interests_in_event(event), user_interests) is not []
