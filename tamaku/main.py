from tamaku.utils.Logger import Logger
from tamaku.tf.TfGetProviders import TfGetProviders

logger = Logger()


def main():
    TfGetProviders()
    logger.info("Terraform providers downloaded successfully")


if __name__ == "__main__":
    main()
