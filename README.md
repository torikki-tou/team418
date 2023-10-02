<h1 class="code-line" data-line-start=0 data-line-end=1 ><a id="__3XUI__Traefik__Telegram_Bot_0"></a>Установка контейнера 3X-UI + Traefik + Telegram Bot</h1>
<p class="has-line-data" data-line-start="1" data-line-end="2">Инструкция будет включать в себя:</p>
<ol>
<li class="has-line-data" data-line-start="3" data-line-end="4">Установка Docker</li>
<li class="has-line-data" data-line-start="4" data-line-end="5">Установка контейнера 3X-UI + Traefik + Telegram Bot</li>
<li class="has-line-data" data-line-start="5" data-line-end="7">Настройка</li>
</ol>
<p class="has-line-data" data-line-start="7" data-line-end="8">Для установки понадобится:</p>
<ol>
<li class="has-line-data" data-line-start="9" data-line-end="10"><strong>VPS или иной сервер с доступом к консоли SSH</strong></li>
<li class="has-line-data" data-line-start="10" data-line-end="11"><strong>1 ГБ ОЗУ</strong></li>
<li class="has-line-data" data-line-start="11" data-line-end="13"><strong>Debian не ниже версии 9 или Ubuntu не ниже 20.04 (инструкция может работать и на других дистрибутивах, но некоторые детали будут отличатся)</strong></li>
</ol>
<p class="has-line-data" data-line-start="13" data-line-end="14">Официальный репозиторий 3X-UI: <a href="https://github.com/MHSanaei/3x-ui">https://github.com/MHSanaei/3x-ui</a></p>
<p class="has-line-data" data-line-start="15" data-line-end="16">Официальный репозиторий форка X-UI: <a href="https://github.com/alireza0/x-ui">https://github.com/alireza0/x-ui</a></p>
<p class="has-line-data" data-line-start="17" data-line-end="18">Для начала необходимо установить Docker и Docker-compose (пропускаем шаг если уже установлен)</p>
<p class="has-line-data" data-line-start="19" data-line-end="20">Добавляем официальный репозиторий Docker:</p>
<p class="has-line-data" data-line-start="21" data-line-end="22">Для Debian:</p>
<pre><code>sudo apt-get update
sudo apt-get install ca-certificates curl gnupg
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

echo \
  &quot;deb [arch=&quot;$(dpkg --print-architecture)&quot; signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian \
  &quot;$(. /etc/os-release &amp;&amp; echo &quot;$VERSION_CODENAME&quot;)&quot; stable&quot; | \
  sudo tee /etc/apt/sources.list.d/docker.list &gt; /dev/null
sudo apt-get update
</code></pre>
<p class="has-line-data" data-line-start="35" data-line-end="36">Для Ubuntu:</p>
<pre><code>sudo apt-get update
sudo apt-get install ca-certificates curl gnupg
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

echo \
  &quot;deb [arch=&quot;$(dpkg --print-architecture)&quot; signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  &quot;$(. /etc/os-release &amp;&amp; echo &quot;$VERSION_CODENAME&quot;)&quot; stable&quot; | \
  sudo tee /etc/apt/sources.list.d/docker.list &gt; /dev/null
sudo apt-get update
</code></pre>
<p class="has-line-data" data-line-start="49" data-line-end="50">Устанавливаем docker и docker-compose:</p>
<pre><code>$ sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
</code></pre>
<p class="has-line-data" data-line-start="53" data-line-end="54">Проверяем работу docker:</p>
<pre><code>$ sudo docker run hello-world
</code></pre>
<p class="has-line-data" data-line-start="59" data-line-end="60">Далее клонируем репозиторий со скриптом установки 3X-UI + Traefik + Telegram Bot:</p>
<pre><code>git clone https://github.com/torikki-tou/team_418.git
cd team_418
</code></pre>
<p class="has-line-data" data-line-start="64" data-line-end="65">Делаем скрипт исполняемым и запускаем установку:</p>
<pre><code>chmod +x setup.sh
./setup.sh
</code></pre>
<p class="has-line-data" data-line-start="69" data-line-end="70">Скрипт запросит у вас:</p>
<p class="has-line-data" data-line-start="71" data-line-end="72">Имя пользователя для панели администратора - “Enter username for 3X-UI Panel”</p>
<p class="has-line-data" data-line-start="73" data-line-end="74">Пароль администратора - “Enter password”</p>
<p class="has-line-data" data-line-start="75" data-line-end="76">Порт подключения к панели администратора - &quot;Enter port on which 3X-UI would be available: &quot;</p>
<p class="has-line-data" data-line-start="77" data-line-end="78">имя хоста (домен) или IP если домен отсутствует “Enter your hostname:”</p>
<p class="has-line-data" data-line-start="79" data-line-end="80">Ваш адрес почты для сертификата LetsEncrypt “Enter your e-mail for certificate:”</p>
<p class="has-line-data" data-line-start="81" data-line-end="82">API токен вашего телеграм бота (подробнее <a href="https://medium.com/geekculture/generate-telegram-token-for-bot-api-d26faf9bf064">тут</a>) “Enter your Telegram bot API token:”</p>
<p class="has-line-data" data-line-start="83" data-line-end="84">По завершении работы скрипт выдаст адрес подключения к панели администратора.</p>
<p class="has-line-data" data-line-start="85" data-line-end="86">3X-UI, Traefik и Telegram бот установлены и работают.</p>
<p class="has-line-data" data-line-start="87" data-line-end="88">Для настройки через Веб UI:</p>
<p class="has-line-data" data-line-start="89" data-line-end="90">Для 3X-UI переходим по адресу <em><a href="https://xn--80ad1e">https://ваш</a></em> домен <em>: ваш порт,</em> где yourserverip - IP-адрес вашего сервера или доменное имя, если оно у вас есть и настроено (обратите внимание, протокол http://, а не https://).</p>
<h3 class="code-line" data-line-start=91 data-line-end=92 ><a id="__91"></a>Создаем подключения</h3>
<p class="has-line-data" data-line-start="93" data-line-end="94"><img src="https://telegra.ph/file/e891341a55991fe203b07.png" alt=""></p>
<p class="has-line-data" data-line-start="95" data-line-end="96">Нажимаем кнопку добавить подключение</p>
<p class="has-line-data" data-line-start="97" data-line-end="98"><img src="https://telegra.ph/file/11891fbceef0a95dff453.png" alt=""></p>
<p class="has-line-data" data-line-start="101" data-line-end="102">Для VLESS с XTLS-Reality:</p>
<p class="has-line-data" data-line-start="103" data-line-end="104">“Remark” (Примечание) - любое название;</p>
<p class="has-line-data" data-line-start="105" data-line-end="106">“Протокол” - “vless”,</p>
<p class="has-line-data" data-line-start="107" data-line-end="108">“Listening IP” (“Порт IP”, который на самом деле не порт, а адрес) - оставляем пустым, либо задаем вручную если надо;</p>
<p class="has-line-data" data-line-start="109" data-line-end="110">“Порт” - вместо случайно выданного ставим 443;</p>
<p class="has-line-data" data-line-start="111" data-line-end="112"><img src="https://habrastorage.org/r/w1560/getpro/habr/upload_files/24b/dd1/97e/24bdd197e359fb064b283c848b767af4.png" alt=""></p>
<p class="has-line-data" data-line-start="113" data-line-end="114">Далее переходим к настройкам клиента.</p>
<p class="has-line-data" data-line-start="115" data-line-end="116">“Email” - это аналог имени пользователя, поэтому стоит указать то, что позволит понять вам к какому пользователю относится конфигурация. Важно: пользователи разных подключений не могут иметь один и тот же email</p>
<p class="has-line-data" data-line-start="117" data-line-end="118">“ID” - генерируется случайно, можно оставить без изменений</p>
<p class="has-line-data" data-line-start="119" data-line-end="120">“Subscription” - тут наоборот, лучше будет если текст в этом поле будет совпадать с тем, что вы задали для Shadowsocks (подробности ниже). <em>Внимание: поле Subscription по умолчанию не отображается, нужно сначала активировать функционал подписок в настройках панели.</em></p>
<p class="has-line-data" data-line-start="121" data-line-end="122">“Flow” - надо выбрать “xtls-rprx-vision”. Обратите внимание, поле Flow (см. скриншот) появится только после того, как чуть ниже вы поставите галочку на пункте “Reality”. То есть лучше всего настривать так: сначала ставите галочку Reality, а потом заполняете поля с настройками пользователя.</p>
<p class="has-line-data" data-line-start="123" data-line-end="124">Дальше у нас идут настройки транспорта:</p>
<p class="has-line-data" data-line-start="125" data-line-end="126">“Reality” - как уже сказано выше, должно быть активно;</p>
<p class="has-line-data" data-line-start="127" data-line-end="128">“XTLS” - наоборот, должно быть неактивно (это немного запутывает, не смотря на то, что Reality тоже относится к XTLS, здесь под XTLS подразумеваются только устаревшие версии протокола, и галочки “XTLS” и “Reality” в панели являются взаимоисключающими);</p>
<p class="has-line-data" data-line-start="129" data-line-end="130">“uTLS” - по умолчанию “firefox”, можно поставить “chrome”, (при выборе “android”, могут быть проблемы с клиентами);</p>
<p class="has-line-data" data-line-start="131" data-line-end="132">“Домен” - на самом деле это не домен, а адрес для подключения к вашему серверу. Можно оставить пустым, тогда панель автоматически подставит IP-адрес или домен, по которому вы обращаетесь в панели на сервере.</p>
<p class="has-line-data" data-line-start="133" data-line-end="134">“ShortIds” - панель сгенерирует рандомный ID;</p>
<p class="has-line-data" data-line-start="135" data-line-end="136">“Public Key”, “Private Key” - можно кликнуть на “Get new keys”, и панель сама сгенерирует новые для вас;</p>
<p class="has-line-data" data-line-start="137" data-line-end="138">“Dest” и “Server names” - вот это самое интересное, это домен, под который вы будете маскироваться. По умолчанию панель предлагает маскировку под <a href="http://yahoo.com">yahoo.com</a> и <a href="http://www.yahoo.com">www.yahoo.com</a> с переадресацией на <a href="http://yahoo.com:443">yahoo.com:443</a>, но лучше выбрать какой-нибудь другой домен, Требования довольно простые:</p>
<p class="has-line-data" data-line-start="139" data-line-end="140">это должен быть иностранный сервер (вне РФ), не заблокированный по домену Роскомнадзором, поддерживающий подключения по TLSv1.3 и HTTP/2, имеющий заглавную страницу, которая <em>не</em> переадресовывает на какой-нибудь другой домен. В идеале если бы IP-адрес был из диапазона того же облачного хостера, что и у вас, и чтобы сервер поддерживал Online Certificate Status Protocol (OCSP). Можно использовать следующие домены:</p>
<ul>
<li class="has-line-data" data-line-start="141" data-line-end="142"><a href="http://www.samsung.com:443">www.samsung.com:443</a></li>
<li class="has-line-data" data-line-start="142" data-line-end="143"><a href="http://www.googletagmanager.com:443">www.googletagmanager.com:443</a></li>
<li class="has-line-data" data-line-start="143" data-line-end="144"><a href="http://www.asus.com:443">www.asus.com:443</a></li>
<li class="has-line-data" data-line-start="144" data-line-end="145"><a href="http://www.amd.com:443">www.amd.com:443</a></li>
<li class="has-line-data" data-line-start="145" data-line-end="146"><a href="http://www.cisco.com:443">www.cisco.com:443</a></li>
<li class="has-line-data" data-line-start="146" data-line-end="147"><a href="http://www.microsoft.com:443">www.microsoft.com:443</a></li>
<li class="has-line-data" data-line-start="147" data-line-end="148"><a href="http://dl.google.com:443">dl.google.com:443</a></li>
<li class="has-line-data" data-line-start="148" data-line-end="149"><a href="http://www.linksys.com:443">www.linksys.com:443</a></li>
<li class="has-line-data" data-line-start="149" data-line-end="151"><a href="http://www.nvidia.com:443">www.nvidia.com:443</a></li>
</ul>
<p class="has-line-data" data-line-start="151" data-line-end="152">и т.д.</p>
<p class="has-line-data" data-line-start="153" data-line-end="154"><img src="https://habrastorage.org/r/w1560/getpro/habr/upload_files/524/938/f6e/524938f6e52c34c0ef374436e120c05f.png" alt=""></p>
<p class="has-line-data" data-line-start="155" data-line-end="156">Сохраняем введенную форму, и - всё! Настройка завершена.</p>
<p class="has-line-data" data-line-start="157" data-line-end="158">После этого на странице видим примерно вот это:</p>
<p class="has-line-data" data-line-start="159" data-line-end="160"><img src="https://telegra.ph/file/7eb8f8013da91cfbfebe0.png" alt=""></p>
<p class="has-line-data" data-line-start="163" data-line-end="164">Если тыкнуть на кнопочку “Меню” соответствующую нужному протоколу, можно его активировать/деактивировать, сбросить счетчики трафика, добавить пользователей (в том числе сгенерировать разом N аккаунтов по шаблону), и самое главное - раскрыв (плюсиком) список пользователей, можно посмотреть настройки подключения для вбивания в клиенты для этого пользователя.</p>
<p class="has-line-data" data-line-start="165" data-line-end="166">Нажав на значок QR-кода, панель покажет QR-код, который можно отсканировать камерой в мобильных клиентах (<a href="https://github.com/2dust/v2rayNG/releases">v2rayNG</a> или <a href="https://github.com/MatsuriDayo/NekoBoxForAndroid/releases">Nekobox</a> на Android, <a href="https://apps.apple.com/us/app/wings-x/id6446119727">Wings X</a>/<a href="https://apps.apple.com/us/app/foxray/id6448898396">FoXray</a> или <a href="https://apps.apple.com/us/app/shadowrocket/id932747118">Shadowrocket</a> на iOS)</p>
