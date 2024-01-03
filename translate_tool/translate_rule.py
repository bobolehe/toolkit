from tools.bing_translate import translateRun
from bs4 import BeautifulSoup
import re


def is_matching_format(text):
    # 定义正则表达式模式
    pattern = r"Upgrade to the latest version of [^ ]+ \(\d+\.\d+\.\d+ or later\) or [^ ]+ \(\d+\.\d+\.\d+ or later\)"

    # 使用正则表达式检查文本是否匹配模式
    return bool(re.match(pattern, text))


def translate_rule(payment_string):
    """
    1、refer to。。。。for，中间的专有英文不要翻译
    2、参考链接：链接地址，修改成参考链接：（回车）链接地址，先判断solution 包不包含see reference 这个字符串，如果包含，对于 see reference 进行机翻，机翻后的修复建议，再添加  参考链接：（回车）链接地址
    3、有多个链接地址的，不要用逗号隔开，要使用回车换行
    4、类似http://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-21406的链接不需要：做判断链接里包含cve.mitre.org域名的链接不追加到修复建议里
    5、Upgrade to the latest version of 。。。。Plugin，中间的专有英文不要翻译
    6、Upgrade to the latest version of 。。。 (1.02 or later)，中间的专有英文不要翻译
    7、from the 。。。 Web site，the和 Web site中间的专有英文不要翻译
    8 Upgrade to the latest version of Россия-3 (4.9.7 or later) or Россия-3 (8.1.2 or later)这种的直接丢给翻译翻
    """
    payment_string = payment_string.strip()
    # 匹配开头和结尾是否为html标签内容
    pattern = re.compile(r'^<[^>]+>.*<\/[^>]+>$', re.DOTALL)
    if pattern.match(payment_string):
        soup = BeautifulSoup(payment_string, 'html.parser')
        # 获取所有标签
        all_tags = soup.find_all()
        i = 0
        t_value = ""
        for tag in all_tags:
            if i:
                i -= 1
                continue
            tag_z_tag = tag.find_all()
            a_text = ''
            if tag_z_tag:
                i = len(tag_z_tag)
                for z in tag_z_tag:
                    if z.name == 'a':
                        a_text += z.get('href')
            t_value += tag.text
            t_value += a_text
            t_value += "\n"
        payment_string = t_value

    # 校验规范1：refer to***for
    ref_to = re.search(r'Refer to (.+?) for', payment_string)
    if ref_to:
        ref_to_str = ref_to.group(1)
        payment_string = payment_string.replace(ref_to_str, "CATP")
        ref_to_str = ref_to_str.strip().replace(",", "、").replace("，", "、").replace("、 and ", "和").replace("", "-").replace(" and ", "和").replace("the ", "")
    else:
        ref_to_str = ""

    ref_to_lower = re.search(r'refer to (.+?) for', payment_string)
    if ref_to_lower:
        ref_to_lower_str = ref_to_lower.group(1)
        payment_string = payment_string.replace(ref_to_lower_str, "ACPT")

        ref_to_lower_str = ref_to_lower_str.strip().replace(",", "、").replace("，", "、").replace("、 and ", "和").replace("", "-").replace(" and ", "和").replace("the ", "")
    else:
        ref_to_lower_str = ""

    # 校验规范3：多个链接地址，使用回车换行
    # payment_string = payment_string.replace(',', '\n')
    upgrade_plugin = re.search(r'Upgrade to the latest version of (.+?) Plugin', payment_string)
    # 校验规范4：Upgrade to the latest version of ***Plugin
    if upgrade_plugin:
        or_exist = is_matching_format(payment_string)
        if or_exist:
            return translateRun.bing_translate(payment_string)
        upgrade_plugin_str = upgrade_plugin.group(1)
        if "," in upgrade_plugin_str:
            pass
        else:
            payment_string = payment_string.replace(upgrade_plugin_str, "ACTP")
    else:
        upgrade_plugin_str = ""

    # 校验规范5：Upgrade to the latest version of *** (1.02 or later)
    upgrade_later = re.search(r'Upgrade to the latest version of (.+?) \(', payment_string)
    if upgrade_later:
        if upgrade_plugin:
            or_exist = is_matching_format(payment_string)
            if or_exist:
                return translateRun.bing_translate(payment_string)
        # 先替换成一些永远不会翻译且还能替换回来的字符.
        upgrade_later_str = upgrade_later.group(1)
        payment_string = payment_string.replace(upgrade_later_str, "TCAP")
        upgrade_later_str = upgrade_later_str.replace(",", "、").replace("，", "、").replace("、 and ", "和").replace("", "-")
    else:
        upgrade_later_str = ""

    # 校验规范6：from the *** Web site
    from_site = re.search(r'from the (.+?) Web site', payment_string)
    if from_site:

        from_site_str = from_site.group(1)
        payment_string = payment_string.replace(from_site_str, "TAPC")
        from_site_str = from_site_str.replace(",", "、").replace("，", "、").replace("、 and ", "和").replace("", "-")
    else:
        from_site_str = ""
    # available_from = re.search(r'from the (.+?) Web site', payment_string)

    if "TCAP" in from_site_str:
        if from_site_str == "TCAP":
            from_site_str = upgrade_later_str
        else:
            from_site_str = from_site_str.replace("TCAP", upgrade_later_str)
    elif "ACTP" in from_site_str:
        if from_site_str == "ACTP":
            from_site_str = upgrade_plugin_str
        else:
            from_site_str = from_site_str.replace("ACTP", upgrade_plugin_str)
    elif "CATP" in from_site_str:
        if from_site_str == "CATP":
            from_site_str = ref_to_str
        else:
            from_site_str = from_site_str.replace("CATP", ref_to_str)
    elif "ACPT" in from_site_str:
        if from_site_str == "ACPT":
            from_site_str = ref_to_lower_str
        else:
            from_site_str = from_site_str.replace("ACPT", ref_to_lower_str)

    from_site_str = from_site_str.strip()
    t_err = translateRun.bing_translate(payment_string)

    if not t_err['status']:
        return {'status': False, 'data': t_err['data']}

    tran_str = t_err['data']
    if "Plugin" in upgrade_later_str:
        upgrade_later_str = upgrade_later_str.replace(" Plugin", "插件")

    tran_str = tran_str.replace("TCAP", upgrade_later_str).replace("ACTP", upgrade_plugin_str).replace("TAPC",
                                                                                                       from_site_str).replace(
        "CATP", ref_to_str).replace("咨询", "公告").replace("参见参考文献。", "参考链接：").replace("请参考链接：",
                                                                                                  "参考链接：").replace(
        "(", "（").replace(")", "）").replace(",", "，").replace(" Web site", "网站").replace("ACPT", ref_to_lower_str).replace("mediawiki标记扩展meetup",
                                                                                                                             "mediawiki-tag-extension-meetup").replace("；", ";")
    tran_str = tran_str.replace("请参阅参考资料。", "参考链接：").replace("参见参考文献", "参考链接：").replace("参见参考文献", "参考链接：")

    return {'status': True, 'data': tran_str}


if __name__ == "__main__":
    # 正常翻译，流程数据
    solution = translate_rule(
        """<p>A remote code execution vulnerability exists when the Windows Print Spooler service improperly performs privileged file operations. An attacker who successfully exploited this vulnerability could run arbitrary code with SYSTEM privileges. An attacker could then install programs; view, change, or delete data; or create new accounts with full user rights.</p>
<p>UPDATE July 7, 2021: The security update for Windows Server 2012, Windows Server 2016 and Windows 10, Version 1607 have been released. Please see the Security Updates table for the applicable update for your system. We recommend that you install these updates immediately. If you are unable to install these updates, see the FAQ and Workaround sections in this CVE for information on how to help protect your system from this vulnerability.</p>
<p>In addition to installing the updates, in order to secure your system, you must confirm that the following registry settings are set to 0 (zero) or are not defined (<strong>Note</strong>: These registry keys do not exist by default, and therefore are already at the secure setting.), also that your Group Policy setting are correct (see FAQ):</p>
<ul>
<li>HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows NT\Printers\PointAndPrint</li>
<li>NoWarningNoElevationOnInstall = 0 (DWORD) or not defined (default setting)</li>
<li>UpdatePromptSettings = 0 (DWORD) or not defined (default setting)</li>
</ul>
<p><strong>Having NoWarningNoElevationOnInstall set to 1 makes your system vulnerable by design.</strong></p>
<p>UPDATE July 6, 2021: Microsoft has completed the investigation and has released security updates to address this vulnerability. Please see the Security Updates table for the applicable update for your system. We recommend that you install these updates immediately. If you are unable to install these updates, see the FAQ and Workaround sections in this CVE for information on how to help protect your system from this vulnerability. See also <a href="https://support.microsoft.com/topic/31b91c02-05bc-4ada-a7ea-183b129578a7">KB5005010: Restricting installation of new printer drivers after applying the July 6, 2021 updates</a>.</p>
<p>Note that the security updates released on and after July 6, 2021 contain protections for CVE-2021-1675 and the additional remote code execution exploit in the Windows Print Spooler service known as “PrintNightmare”, documented in CVE-2021-34527.</p>
""")
    # Upgrade to the latest version of Broadpeak Centralized Accounts Management Auth Agent, available from the Broadpeak Web site. See References.
    # https://broadpeak.tv/ 网站上提供的
    # CVE-2023-44145插件强行翻译
    # CVE-2019-14467强行翻译
    # 找CVE-2022-0781和CVE-2022-3334两个的区别

    print(solution)
