from PIL import ImageGrab, Image
from time import time, sleep
import requests


def main():
    checker = PfChecker(party_size=8)
    checker.monitor(check_interval=5)


class PfChecker:
    def __init__(self, party_size):
        self.party_size = party_size
        self.top_loc = (370, 682)  # px configure this
        self.vertical_spacing = 40  # px configure this
        self.color_accuracy = 7  # 0 = exact
        self.members = 1
        self.webhook_url = "Put your own webhook here"

    def get_screen(self):
        self.screen = ImageGrab.grab()

    def get_image(self, path):
        self.screen = Image.open(path)

    def count_members(self):
        self.get_screen()
        members = 1
        #base_relative_color = self.screen.getpixel(self.top_loc)
        base_color = (232, 209, 155)  # Job token color
        # base_color = (255, 255, 255) # hp bar color
        disabled_color = (163, 151, 118)  # Disabled job token color
        self.color_list = [base_color]
        for i in range(1, self.party_size):
            test_color = self.screen.getpixel((self.top_loc[0], self.top_loc[1] + (i) * self.vertical_spacing))
            self.color_list.append(test_color)

            # Check if colors match
            for base, disabled, test in zip(base_color, disabled_color, test_color):
                if abs(base - test) < self.color_accuracy:
                    is_member = True
                    continue
                elif abs(disabled - test) < self.color_accuracy:
                    is_member = True
                    continue
                else:
                    is_member = False
                    break
            if is_member:
                members += 1
        self.members = members

    def monitor(self, check_interval=60):
        print("Starting continous monitoring of party members")
        self.time_started = time()
        self.max_time = 3600  # 1 hour pf limit

        while True:
            self.time_left = self.max_time - (time() - self.time_started)
            self.count_members()
            print("\n" * 3)
            print(f"Party members: {self.members}")
            for i in self.color_list:
                print(i)
            if self.members == self.party_size:
                self.notify_gamer("Party has filled!")
            elif self.time_left < 300:
                self.notify_gamer("Time running out!")
            sleep(check_interval)

    def notify_gamer(self, message):
        while True:
            print(f"Message to gamer: {message}")
            response = requests.get(self.webhook_url)
            print(response)
            sleep(30)


if __name__ == '__main__':
    main()
