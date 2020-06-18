from dns import resolver
from asyncio.subprocess import PIPE, create_subprocess_exec
from requests.exceptions import ConnectionError
from TheDigger_src.utils.help_utils import HelpUtilities
from TheDigger_src.utils.exceptions import TheDiggerException
from TheDigger_src.utils.logger import Logger
from TheDigger_src.utils.coloring import COLOR, COLORED_COMBOS


# noinspection PyUnboundLocalVariable
class DNS_Handler:
    """Handles Lookups and DNS queries"""

    resolver = resolver.Resolver()

    @classmethod
    def query_dns(cls, domains, records):
        """
        Query DNS records for host.
        :param domains: Iterable of domains to get DNS Records for
        :param records: Iterable of DNS records to get from domain.
        """
        results = {k: set() for k in records}
        for record in records:
            for domain in domains:
                try:
                    answers = cls.resolver.query(domain, record)
                    for answer in answers:
                        # Add value to record type
                        results.get(record).add(answer)
                except (resolver.NoAnswer, resolver.NXDOMAIN, resolver.NoNameservers):
                    # Type of record doesn't fit domain or no answer from NameServer
                    continue

        return {k: v for k, v in results.items() if v}

    @classmethod
    async def grab_whois(cls, host):
        if not host.naked:
            return

        script = "whois {}".format(host.naked).split()
        log_file = HelpUtilities.get_output_path("{}/whois.txt".format(host.target))
        logger = Logger(log_file)

        process = await create_subprocess_exec(
            *script,
            stdout=PIPE,
            stderr=PIPE
        )
        result, err = await process.communicate() #err has not been used, Please make sure to implement the variable. 

        if process.returncode == 0:
            logger.info("{} {} WHOIS information has been retrieved".format(COLORED_COMBOS.GOOD, host))
            for line in result.decode().strip().split("\n"):
                    if ":" in line:
                        logger.debug(line)

    @classmethod
    async def generate_dns_dumpster_mapping(cls, host, sout_logger):
        sout_logger.info("{} DNS Dumpster is fetching data for {} ".format(
            COLORED_COMBOS.INFO, host))
        try:
            page = HelpUtilities.query_dns_dumpster(host=host)
            if page.status_code == 200:
                path = HelpUtilities.get_output_path("{}/dns_mapping.png".format(host.target))
                with open(path, "wb") as target_image:
                    target_image.write(page.content)
                sout_logger.info("{} DNS Mapping sucessfully fetched for {}".format(
                    COLORED_COMBOS.GOOD, host.target)
                )
            else:
                raise TheDiggerException
        except TheDiggerException:
            sout_logger.info("{} DNS Mapping has Failed. There is a connection error.".format(
                COLORED_COMBOS.BAD))
