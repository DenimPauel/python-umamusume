# This Python file uses the following encoding: utf-8
# 解像度 960x540 で作ってあるので、実行前にNoxの解像度を変更して下さい。

# pip install android-auto-play-opencv
import android_auto_play_opencv as am
import datetime
#import inquirer  # pip install inquirer

import os
adbpathCandidates = [
    'C:\\Program Files\\Nox\\bin\\',
    'C:\\Program Files (x86)\\Nox64\\bin\\',
    'C:\\Program Files (x86)\\Nox\\bin\\'
]

# ログ機能
from logging import getLogger, StreamHandler, FileHandler, DEBUG, Formatter
logger = getLogger( __name__ )
logger.setLevel(DEBUG)

hFile = FileHandler( 'resetMarathon.log' )
hFile.setLevel(DEBUG)
format_file = Formatter('%(asctime)s - %(name)s - %(levelname)s : %(message)s')
hFile.setFormatter(format_file)

logger.addHandler(hFile)

hConsole = StreamHandler()
hConsole.setLevel(DEBUG)
format_console = Formatter('%(message)s')
hConsole.setFormatter(format_console)
logger.addHandler(hConsole)

logger.propagate = False

aapo = None

# ターゲットガチャの選択
GET_PRETTY_DARBY_GATYA = True  # サポートガチャをターゲットにする場合は、Falseにする。

if GET_PRETTY_DARBY_GATYA == True:
    # 20210828現在、無料ガチャは、プリティガチャの先なので、左から
    GATYA_PAGE_FEED_CW = False  # サポートガチャをページ送り方向(False:左周り)
else:
    GATYA_PAGE_FEED_CW = True  # サポートガチャをページ送り方向(True:右周り)


def main():

    global aapo
    for i in range(len(adbpathCandidates)):
        if( os.path.exists(adbpathCandidates[i]) == True ):
            adbpath=adbpathCandidates[i]
            break
    aapo = am.AapoManager(adbpath)
    mode = 0  # モード0(リセット)
    folderName = ''
    stackCount = 0
    present_ok = False

    robyCount = 0  # ロビーカウンタ(変数の初期化)
    robyStable = 5  # ロビー安定を判断する回数

    # ↓複数デバイスを同時に操作したい場合、コメントを外す。
    #devicesselect = [
    #    inquirer.List(
    #        "device",
    #        message="デバイスを選択して下さい。",
    #        choices=aapo.adbl.devices
    #    )
    #]
    #selected = inquirer.prompt(devicesselect)
    #aapo.adbl.setdevice(selected['device'])

    # スタート
    start()

    while True:
        # 画面キャプチャ
        aapo.screencap()

        # 早送りボタンは常にタップ
        if aapo.touchImg('./umamusume/hayaokuri.png'):
            # タップ出来たら待機
            logger.info( '早送りアイコン検出、早送りをタップ' )
            aapo.sleep(1)

        # 通信エラー時は、タイトルへを押す)
        elif aapo.chkImg('./umamusume/communicationerror.png'):
            logger.info( '通信エラー時は、タイトルへをタップ' )
            aapo.touchImg('./umamusume/tothetitle.png')
            aapo.sleep(1)

        # Google Playダイアログが出たら、キャンセルボタンをタップ
        elif aapo.chkImg('./umamusume/google-play.png'):
            logger.info( 'Google Playダイアログ検出、キャンセルをタップ' )
            aapo.touchImg('./umamusume/cancel.png')
            aapo.sleep(1)

        # アカウント連携ダイアログが出たら、後でするボタンをタップ
        elif aapo.chkImg('./umamusume/account.png'):
            logger.debug( 'アカウント連携ダイアログ検出、後でするをタップ' )
            aapo.touchImg('./umamusume/atode.png')
            aapo.sleep(1)

        # チュートリアルダイアログが出たら、スキップボタンをタップ
        elif aapo.chkImg('./umamusume/tutorial.png'):
            logger.info( 'チュートリアルダイアログ検出、スキップをタップ' )
            aapo.touchImg('./umamusume/skip.png')
            aapo.sleep(1)

        # トレーナー登録ダイアログが出たら、
        elif aapo.chkImg('./umamusume/trainer.png'):
            # トレーナー名入力の位置をタップ
            aapo.touchPos(405, 430)
            aapo.sleep(1)
            # abc と入力
            aapo.inputtext('abc')
            aapo.sleep(1)
            # トレーナー名入力の位置をタップ
            aapo.touchPos(270, 430)
            aapo.sleep(1)
            # 登録ボタンの位置をタップ1
            aapo.touchPos(270, 630)
            aapo.sleep(1)
            # 登録ボタンの位置をタップ2
            aapo.touchPos(270, 630)
            aapo.sleep(1)
            # OKボタンの位置をタップ
            aapo.touchPos(405, 630)
            aapo.sleep(1)

        # データダウンロードダイアログが出たら、OKボタンをタップ
        elif aapo.chkImg('./umamusume/datadownload.png'):
            logger.info( 'データダウンロードダイヤログ検出、OKをタップ' )
            aapo.touchImg('./umamusume/ok.png')
            aapo.sleep(1)

        # お知らせダイアログが出たら、閉じるボタンをタップ
        elif aapo.chkImg('./umamusume/osirase.png'):
            logger.info( 'お知らせダイヤログ検出、閉じるをタップ' )
            aapo.touchImg('./umamusume/close.png')
            aapo.sleep(1)

        # メインストーリー開放ダイアログが出たら、閉じるボタンをタップ
        elif aapo.chkImg('./umamusume/main-story.png'):
            logger.info( 'メインストーリー開放ダイヤログ検出、閉じるをタップ' )
            aapo.touchImg('./umamusume/close.png')
            aapo.sleep(1)

        # ウマ娘ストーリー開放ダイアログが出たら、閉じるボタンをタップ
        elif aapo.chkImg('./umamusume/umamusume-story.png'):
            logger.info( 'ウマ娘ストーリー開放ダイヤログ検出、閉じるをタップ' )
            aapo.touchImg('./umamusume/close.png')
            aapo.sleep(1)

        # ウマ娘詳細ダイアログが出たら、閉じるボタンをタップ
        elif aapo.chkImg('./umamusume/umamusume-syosai.png'):
            logger.info( 'ウマ娘詳細ダイヤログ検出、閉じるをタップ' )
            aapo.touchImg('./umamusume/close.png')
            aapo.sleep(1)

        # 日付が変わりましたが表示されたら、
        elif aapo.chkImg('./umamusume/newday.png'):
            logger.info( '日付が変わりました検出、OKをタップ' )
            aapo.touchImg('./umamusume/OK.png')
            aapo.sleep(1)

        # 受取完了ダイアログが出たら、閉じるの位置をタップ
        elif aapo.chkImg('./umamusume/uketorikanryo.png'):
            logger.info( '受取完了ダイヤログ検出、閉じるをタップ' )
            aapo.touchImg('./umamusume/close.png')
            aapo.sleep(1)

        # 衣装獲得ダイアログが出たら、閉じるの位置をタップ
        elif aapo.chkImg('./umamusume/isyoget.png'):
            logger.info( 'ウマ娘詳細ダイヤログ検出、閉じるをタップ' )
            aapo.touchImg('./umamusume/close.png')
            aapo.sleep(1)

        # プレゼントダイアログが出たら、一括受取の位置をタップ
        elif aapo.chkImg('./umamusume/present.png') and present_ok == False:
            logger.info( 'プレゼントダイアログが出たら、一括受取の位置をタップ' )
            aapo.touchImg('./umamusume/ikkatuuketori1.png')
            present_ok = True
            aapo.sleep(1)

        # プレゼントを受け取った後で一括受取が押せなくなったら、閉じるの位置をタップ
        elif aapo.chkImg('./umamusume/ikkatuuketori2.png') and present_ok == True:
            logger.info( 'プレゼントを受け取った後で一括受取が押せなくなったら、閉じるの位置をタップ' )
            aapo.touchImg('./umamusume/close.png')
            aapo.sleep(1)

        # ガチャボタンを見つけたら、ロビーと判断し、プレゼントを受け取っていない場合、
        elif aapo.chkImg('./umamusume/roby.png') and present_ok == False:

            # お知らせが差し込まれる場合があるため、ロービーが安定するまで、robyStable回空ループさせる。
            robyCount += 1
            if robyCount < robyStable:
                logger.info( 'ガチャボタンを見つけた'+ str(robyCount) )
                aapo.sleep(1)  # 小休止を入れる
                continue
            else:
                logger.info( 'ガチャボタンを見つけた'+ str(robyCount) + 'ロビーと判断。robyCountリセット')
                robyCount = 0

            # プレゼントの位置をタップ
            aapo.touchPos(490, 680)
            aapo.sleep(1)

        # ガチャボタンを見つけたら、ロビーと判断し、プレゼントを受け取った後、
        elif aapo.chkImg('./umamusume/roby.png') and present_ok == True:

            # 実績ログが終わるまで待機（メニューボタンが隠れて押せないから）
            robyCount += 1
            if robyCount < robyStable:
                logger.info( 'ガチャボタンを見つけた(プレゼント受領後)'+ str(robyCount) )
                aapo.sleep(1)  # 小休止を入れる
                continue
            else:
                logger.info( 'ガチャボタンを見つけた(プレゼント受領後)'+ str(robyCount) + 'ロビーと判断。robyCountリセット'  )
                robyCount = 0

            # メニューボタンの位置をタップ
            aapo.touchPos(490, 50)
            aapo.sleep(1)
            # データ連携の位置をタップ1
            aapo.touchPos(410, 640)
            aapo.sleep(1)
            # データ連携の位置をタップ2
            aapo.touchPos(405, 640)
            aapo.sleep(1)
            # 連携パスワードの位置をタップ
            aapo.touchPos(450, 550)
            aapo.sleep(1)
            # 設定の位置をタップ
            aapo.touchPos(405, 640)
            aapo.sleep(1)
            # 連携パスワード入力の位置をタップ
            aapo.touchPos(270, 405)
            aapo.sleep(1)
            # 1qazXSW2 と入力
            aapo.inputtext('1qazXSW2')
            aapo.sleep(1)
            # 確認入力の位置をタップ1
            aapo.touchPos(270, 505)
            aapo.sleep(1)
            # 確認入力の位置をタップ2
            aapo.touchPos(270, 505)
            aapo.sleep(1)
            # 1qazXSW2 と入力
            aapo.inputtext('1qazXSW2')
            aapo.sleep(1)
            # プライバシーポリシーの位置をタップ1
            aapo.touchPos(135, 620)
            aapo.sleep(1)
            # プライバシーポリシーの位置をタップ2
            aapo.touchPos(135, 620)
            aapo.sleep(1)
            # OKの位置をタップ
            aapo.touchPos(405, 680)
            aapo.sleep(1)
            # 画面キャプチャ
            aapo.screencap()
            # フォルダ名がカラの場合セット
            if len(folderName) == 0:
                folderName = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
            # スクショを保存
            aapo.imgSave('gatya/' + folderName + '/screenshot_' +
                         datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '.png')
            aapo.sleep(1)
            # 閉じるの位置をタップ
            aapo.touchPos(270, 630)
            aapo.sleep(3)
            # ガチャボタンの位置をタップ
            aapo.touchPos(480, 930)
            aapo.sleep(2)

        # 無料ガチャボタンがあれば引く。
        elif aapo.touchImg('./umamusume/onegatyaforfree.png'):
            logger.info( '無料ガチャを1回引く！' )
            # タップ出来たら待機
            aapo.sleep(1)

        # ガチャを引く！
        elif aapo.touchImg('./umamusume/gatyahiku.png'):
            logger.info( 'ガチャを1回引く！' )
            # タップ出来たら待機
            aapo.sleep(1)

        # ガチャ結果
        elif aapo.chkImg('./umamusume/gatya-kekka.png'):
            logger.info( 'ガチャ結果' )
            # フォルダ名がカラの場合セット
            if len(folderName) == 0:
                folderName = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
            # スクショを保存
            aapo.screencap()    #スクリーンリフレッシュ（写真が取れない場合がある。ボタン押下時のタイマーよりここのほうが確実な気がする。)
            aapo.imgSave('gatya/' + folderName + '/screenshot_' +
                         datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '.png')
            aapo.sleep(1)

            # もう1回引くボタンをタップ
            if aapo.touchImg('./umamusume/pickagain.png'):
                logger.info( 'もう1回引くをタップ' )
                aapo.sleep(1)
            # または、OKボタンをタップ（無料ガチャのケース）
            elif aapo.touchImg('./umamusume/ok.png'):
                logger.info( 'OKをタップ' )
                aapo.sleep(1)

        # 購入するボタンが出たら、ガチャ終了
        elif aapo.chkImg('./umamusume/konyusuru.png'):
            logger.info( '購入するボタンが出たらガチャ終了' )
            # リセット
            reset()
            # スタート
            start()

            mode = 0  # モード0(リセット)
            folderName = ''
            stackCount = 0
            robyCount = 0
            present_ok = False

        # 左上ピンクのガチャタイトルが出たら、対象ガチャのページに移動、10連ガチャボタンを表示させる
        elif aapo.chkImg('./umamusume/gatyaselected.png'):
            logger.info( 'ガチャページタイトル検出' )
            if GET_PRETTY_DARBY_GATYA:
                found = aapo.chkImg('./umamusume/gatyaprettydarby.png')
            else:
                found = aapo.chkImg('./umamusume/gatyasupportcard.png')

            if found:
                logger.info( 'ターゲットガチャページ到着。10回引く！' )
                # 10回引く！
                aapo.touchImg('./umamusume/10-kaihiku.png')
            else:
                # 次のページへ
                logger.info( 'ターゲットガチャページ未到着。ページ変更。' )
                if GATYA_PAGE_FEED_CW:
                    aapo.touchPos(460, 580)    # > 右周り
                else:
                    aapo.touchPos(80, 580)    # < 左周り

            aapo.sleep(1)

        # モードが0(リセット)の場合
        elif mode == 0:
            # ハンバーガーメニューボタンをタップ
            if aapo.touchImg('./umamusume/hanba-ga-menu.png'):
	            #logger.info( 'モードが0(リセット)ハンバーガーメニューボタンをタップ' )
                # タップ出来たら待機
                aapo.sleep(1)
                # ユーザーデータ削除の位置をタップ1
                aapo.touchPos(270, 750)
                aapo.sleep(1)
                # ユーザーデータ削除の位置をタップ2
                aapo.touchPos(405, 630)
                aapo.sleep(1)
                # ユーザーデータ削除の位置をタップ3
                aapo.touchPos(405, 630)
                aapo.sleep(1)
                # 閉じるの位置をタップ
                aapo.touchPos(270, 630)
                aapo.sleep(1)
                # モードを1(チュートリアル)に変更
                mode = 1

        # モードが1(チュートリアル)の場合
        elif mode == 1:
            # ロゴをタップ
            if aapo.touchImg('./umamusume/logo.png'):
                logger.info('モード1 ロゴをタップ')
                # タップ出来たら待機
                aapo.sleep(1)

            # 同意をタップ
            elif aapo.touchImg('./umamusume/doui.png'):
                logger.info( 'モード1 同意をタップ' )
                # タップ出来たら待機
                aapo.sleep(1)

        # スタック対策 起動後STARTが表示されない、アンドロイド画面(アプリが落ちた場合)
        if aapo.chkImg('./umamusume/stack.png') or aapo.chkImg('./umamusume/umamusumegameicon.png'):
            aapo.sleep(1)
            stackCount = stackCount + 1
            if stackCount > 10:
                logger.info( 'スタック判定' )
                # リセット
                reset()
                # スタート
                start()

                mode = 0  # モード0(リセット)
                folderName = ''
                stackCount = 0
                robyCount = 0
                present_ok = False
        else:
            stackCount = 0


def start():
    # アプリ起動
    aapo.start(
        'jp.co.cygames.umamusume/jp.co.cygames.umamusume_activity.UmamusumeActivity')
    aapo.sleep(10)
    return


def reset():
    # ホームキーを押す
    aapo.inputkeyevent(3)
    aapo.sleep(1)
    # タスクキーを押す
    aapo.inputkeyevent(187)
    aapo.sleep(1)
    # すべて消去の位置をタップ
    aapo.touchPos(700, 55)
    aapo.sleep(1)

    # ウマ娘アイコンを探して、ロングタップ、キャッシュを消す
    aapo.screencap()
    found, x, y = aapo.chkImg2('./umamusume/umamusumeGameIcon.png')
    if found:
        logger.info( 'デスクトップ上に、ウマ娘アイコン検出')
        aapo.longTouchPos(x, y, 1000)
        aapo.sleep(1)

        # プロパティ表示
        aapo.screencap()
        aapo.touchImg('./umamusume/appproperty.png')
        aapo.sleep(1)

        # ストレージ表示
        aapo.screencap()
        aapo.touchImg('./umamusume/calculatingstorage.png')
        aapo.sleep(1)

        # キャッシュを削除
        aapo.screencap()
        aapo.touchImg('./umamusume/clearcache.png')
        aapo.sleep(1)

        # タスクキーを押す
        aapo.inputkeyevent(187)
        aapo.sleep(1)
        # すべて消去の位置をタップ
        aapo.touchPos(700, 55)
        aapo.sleep(1)

    return


if __name__ == '__main__':
    main()
