# ! / usr / bin / trăn
# mã hóa = utf-8
nhập omeplib2
nhập khẩu json
nhập khẩu lại
nhập khẩu urllib
nhập khẩu os
nhập khẩu uuid
nhập ngữ cảnh
nhập zipfile
nhập ngẫu nhiên
cơ sở nhập khẩu64
thời gian nhập khẩu
nhập chủ đề
ổ cắm nhập khẩu
từ datetime nhập datetime
# Tham họa xbmcswift2 khung cho kodi addon
# http://xbmcswift2.readthedocs.io/en/latest/
từ Plugin nhập kodiswift , xbmc, xbmcaddon, xbmcgui, hành động, xbmcplugin
đường dẫn = xbmc.translatePath (
	xbmcaddon.Addon (). getAddonInfo ( ' path ' )). giải mã ( " utf-8 " )
cache = xbmc.translatePath (os.path.join (đường dẫn, " .cache " ))
tmp = xbmc.translatePath ( ' đặc biệt: // temp ' )
addons_folder = xbmc.translatePath ( ' đặc biệt: // home / addons ' )
image = xbmc.transTablePath (os.path.join (đường dẫn, " icon.png " ))

plugin = Plugin ()
addon = xbmcaddon.Addon ( " plugin.video.tranhuyhoang.playlist " )
pluginrootpath =  " plugin: //plugin.video.tranhuyhoang.playlist "
http = httplib2.Http (bộ nhớ cache, disable_ssl_certificate_validation = Đúng )
query_url =  " https://docs.google.com/s Lansheet / d/ {sid} / gviz / tq? gid = {gid} & headers = 1 & tq = {tq} "
sheet_headers = {
	"Tác nhân người dùng " : " Mozilla / 5.0 (tương thích; MSIE 10.0; Windows NT 6.3; WOW64; Trident / 7.0) " ,
	" Chấp nhận mã hóa " : " gzip, giảm phát, sdch "
}


def  GetSheetIDFromSinstall ():
	sid =  " 13zUxgD6SfGj1YmRa9RU4Vu1AgVv8EaBAsBP3MxEpXOY "
	resp, content = http.request (get_fshare_setting ( " GSheetURL " ), " ĐẦU " )
	thử :
		sid = re.compile ( " /d/(.+?)/ " ) .findall (resp [ " nội dung-vị trí " ]) [ 0 ]
	ngoại trừ :
		vượt qua
	trở sid


def  M3UToItems ( url_path = " " ):
	'' '
	Danh sách phát m3u danh sách hát xbmcswift2
	Thông số
	----------
	url_path: chuỗi
		liên kết danh sách nhạc dung dung m3u
	'' '
	item_V =  ' \ #EXTINF (. *?,) (. *?) \ n (. *?) \ n '
	(tương ứng, nội dung) = http.request (
		url_path, " NHẬN " ,
		tiêu đề = sheet_headers
	)
	vật phẩm = []
	matchs = re.compile (item_re) .findall (nội dung)
	để biết thông tin, nhãn, đường dẫn trong trận đấu:
		ngón tay cái =  " "
		nhãn2 =  " "
		nếu  " tvg-logo "  trong thông tin:
			thumb = re.compile ( ' tvg-logo = \ " ? (. *?) \" ?, ' ) .findall (thông tin) [ 0 ]
		nếu  " tiêu đề nhóm "  trong thông tin:
			nhãn2 = re.compile ( ' group-title = "(. *?)" ' ) .findall (thông tin) [ 0 ]
		nếu nhãn2 ! =  " " :
			nhãn2 =  " [ % s ] "  % nhãn2.strip ()
		nhãn =  " % s% s "  % (nhãn2, nhãn.strip ())
		mục = {
			" nhãn " : nhãn,
			" hình thu nhỏ " : thumb.strip (),
			" đường dẫn " : path.strip (),
		}

		# Danh là liên kết có thể chơi được
		if  " : // "  trong mục [ " path " ]:
			# Liên kết plugin plugin: //
			if item [ " path " ] .startswith ( " plugin: // " ):
				mục [ " is_playable " ] =  Đúng
				mục [ " thông tin " ] = { " loại " : " video " }
			# Liên kết mạng .ts
			elif re.search ( " \ .ts $ " , mục [ " đường dẫn " ]):
				item [ " path " ] =  " plugin: //plugin.video.f4mTester/? url = % s & streamtype = TSDOWNLOADER & use_proxy_for_chunks = True & name = % s "  % (
					urllib.quote (mục [ " đường dẫn " ]),
					urllib.quote_plus (mục [ " nhãn " ])
				)
				mục [ " đường dẫn " ] = pluginrootpath + \
					" / execebuiltin / "  + urllib.quote_plus (mục [ " đường dẫn " ])
			# Liên kết trực tiếp
			khác :
				nếu  " acestream "  trong mục [ " đường dẫn " ]:
					mục [ " nhãn " ] =  " [AceStream] % s "  % item [ " nhãn " ]
				mục [ " đường dẫn " ] = pluginrootpath + \
					" / play / % s "  % urllib.quote_plus (mục [ " đường dẫn " ])
				mục [ " is_playable " ] =  Đúng
				mục [ " thông tin " ] = { " loại " : " video " }
		khác :
			# Không cần phải ...
			mục [ " is_playable " ] =  Sai

		# Hack mục xbmcswift2 để đặt cả is_playable và is_folder thành Sai
		# Cần thiết cho f4mTester
		nếu  " f4mTester "  trong mục [ " đường dẫn " ]:
			mục [ " is_playable " ] =  Sai
		mục + = [mục]
	trả lại hàng


@ plugin.cached ( ttl = 525600 )
def  getCachedItems ( url_path = " 0 " ):
	trả về AddTracking (getItems (url_path))


def  getItems ( url_path = " 0 " , tq = " chọn A, B, C, D, E " ):
	'' '
	Các mục trên mạng theo từ xbmcswift2 từ Bảng tính Google
	Thông số
	----------
	url_path: chuỗi
		Từ khóa "gid" của kho lưu trữ:
			Cài đặt tự động và repo trong bảng Kho
		Liên kết tải xuống zip repo
			Tải xuống và cài đặt zip repo tinh
	theo dõi chuỗi: chuỗi
		 Tên tập tin xem của
	'' '
	# Mặc định VN Mở danh sách phát ID

	sheet_id = GetSheetIDFromSinstall ()
	gid = url_path
	nếu  " @ "  trong url_path:
		path_split = url_path.split ( " @ " )
		gid = path_split [ 0 ]
		sheet_id = path_split [ 1 ]
	history = plugin.get_st Storage ( ' history ' )
	nếu  " nguồn "  trong lịch sử:
		history [ " nguồn " ] = [ " https://docs.google.com/s Lansheet / d / % s / chỉnh sửa # gid = % s "  %
                        (sheet_id, gid)] + history [ " nguồn " ]
		history [ " nguồn " ] = history [ " nguồn " ] [ 0 : 4 ]
	khác :
		lịch sử [ " nguồn " ] = [
			" https://docs.google.com/s  Lansheet / d / % s / chỉnh sửa # gid = % s " % (sheet_id, gid)]
	url = query_url.format (
		sid = sheet_id,
		TQ = urllib.quote (TQ),
		gid = gid
	)
	(tương ứng, nội dung) = http.request (
		url, " NHẬN " ,
		tiêu đề = sheet_headers
	)
	_re =  " google.visualization.Query.setResponse \ ((. +) \); "
	_json = json.loads (re.compile (_re) .findall (nội dung) [ 0 ])
	vật phẩm = []
	cho hàng trong _json [ " bảng " ] [ " hàng " ]:
		mục = {}
		mục [ " nhãn " ] = getValue (hàng [ " c " ] [ 0 ]). mã hóa ( " utf-8 " )
		mục [ " nhãn2 " ] = getValue (hàng [ " c " ] [ 4 ])
		# Nếu phát hành Bảng tính trong trò chơi VNOpenPlaylist
		new_path = getValue (hàng [ " c " ] [ 1 ])
		nếu  " @ "  trong url_path và  " @ "  không có  trong new_path và  " phần / "  trong new_path:
			gid = re.compile ( " phần / (\ d +) " ) .findall (new_path) [ 0 ]
			new_path = re.sub (
				' phần / \ d + ' ,
				' phần / % s @ % s '  % (gid, sheet_id),
				con đường mới,
				cờ = tái. BỎ QUA TRƯỜNG HỢP
			)
		mục [ " đường dẫn " ] = new_path

		mục [ " hình thu nhỏ " ] = getValue (hàng [ " c " ] [ 2 ])
		mục [ " thông tin " ] = { " âm mưu " : getValue (hàng [ " c " ] [ 3 ])}
		nếu  " plugin: // "  trong mục [ " path " ]:
			nếu  " install-repo "  trong mục [ " path " ]:
				mục [ " is_playable " ] =  Sai
			elif re.search ( " plugin.video.tranhuyhoang.playlist / (. +?) /.+?\:// " , mục [ " path " ]):
				phù hợp = nghiên cứu lại (
					" plugin.video.tranhuyhoang.playlist (/.+?/). +? \: // " , mục [ " đường dẫn " ])
				tmp = item [ " đường dẫn " ] .split (match.group ( 1 ))
				tmp [ - 1 ] = urllib.quote_plus (tmp [ - 1 ])
				mục [ " đường dẫn " ] = match.group ( 1 ) .join (tmp)
				if  " / play / "  trong match.group ( 1 ):
					mục [ " is_playable " ] =  Đúng
					mục [ " thông tin " ] = { " loại " : " video " }
			mục elif [ " đường dẫn " ] .startswith ( " plugin: //plugin.video.f4mTester " ):
				mục [ " is_playable " ] =  Sai
				mục [ " đường dẫn " ] = pluginrootpath + \
					" / execebuiltin / "  + urllib.quote_plus (mục [ " đường dẫn " ])
			elif  " / play / "  trong mục [ " path " ]:
				mục [ " is_playable " ] =  Đúng
				mục [ " thông tin " ] = { " loại " : " video " }
		mục elif [ " đường dẫn " ] ==  " " :
			mục [ " nhãn " ] =  " [I] % s [/ I] "  % mục [ " nhãn " ]
			mục [ " is_playable " ] =  Sai
			mục [ " path " ] = pluginrootpath +  " / execebuiltin / - "
		khác :
			nếu  " bảng tính / d / "  trong mục [ " đường dẫn " ]:
				# https://docs.google.com/s Lansheet / d / 13zUxgD6SfGj1YmRa9RU4Vu1AgVv8EaBAsBP3MxEpXOY/edit # gid=0
				match_cache = re.search ( ' cache = (. +?) ($ | &) ' , mục [ " đường dẫn " ])
				match_passw = re.search ( ' passw = (. +?) ($ | &) ' , mục [ " đường dẫn " ])

				sheet_id = re.compile ( " /d/(.+?)/ " ) .findall (mục [ " đường dẫn " ]) [ 0 ]
				thử :
					gid = re.compile ( " gid = (\ d +) " ) .findall (mục [ " đường dẫn " ]) [ 0 ]
				ngoại trừ :
					gid =  " 0 "
				mục [ " đường dẫn " ] = pluginrootpath +  " / phần / % s @ % s "  % (gid, sheet_id)
				nếu match_cache:
					cache_version = match_cache.group ( 1 )
					mục [ " đường dẫn " ] = pluginrootpath + \
						" / bộ nhớ cache / % s @ % s @ % s "  % (gid, sheet_id, cache_version)
				elif match_passw:
					mục [ " đường dẫn " ] = pluginrootpath + \
						" / phần mật khẩu / % s / % s @ % s "  % (match_passw.group ( 1 ), gid, sheet_id)
			elif re.search ( r ' textuploader ' , mục [ " path " ]):
				mục [ " đường dẫn " ] = pluginrootpath + \
					" / m3u / "  + urllib.quote_plus (mục [ " đường dẫn " ])
			elif  any (dịch vụ trong mục [ " path " ] cho dịch vụ trong [ " acel hiện.in " ]):
				mục [ " đường dẫn " ] = pluginrootpath + \
					" / acelist / "  + urllib.quote_plus (mục [ " đường dẫn " ])
			elif  bất kỳ (dịch vụ trong mục [ " con đường " ] cho dịch vụ trong [ " fshare.vn/folder " ]):
				mục [ " đường dẫn " ] = pluginrootpath +  " / fshare / "  + \
					urllib.quote_plus (mục [ " đường dẫn " ] .encode ( " utf8 " ))
				# item ["path"] = "plugin: //plugin.video.xshare/? mode = 90 & page = 0 & url =" + urllib.quote_plus (mục ["path"])
			elif  bất kỳ (dịch vụ trong mục [ " con đường " ] cho dịch vụ trong [ " 4share.vn/d/ " ]):
				mục [ " path " ] =  " plugin: //plugin.video.xshare/? mode = 38 & page = 0 & url = "  + \
					urllib.quote_plus (mục [ " đường dẫn " ])
			elif  bất kỳ (dịch vụ trong mục [ " con đường " ] cho dịch vụ trong [ " 4share.vn/f/ " ]):
				# elif any (dịch vụ trong mục ["đường dẫn"] cho dịch vụ trong ["4share.vn/f/", "fshare.vn/file"]):
				item [ " path " ] =  " plugin: //plugin.video.xshare/? mode = 3 & page = 0 & url = "  + \
					urllib.quote_plus (mục [ " đường dẫn " ])
				mục [ " is_playable " ] =  Đúng
				mục [ " thông tin " ] = { " loại " : " video " }
				mục [ " đường dẫn " ] = pluginrootpath +  " / play / "  + urllib.quote_plus (mục [ " đường dẫn " ])
			elif  " youtube.com/channel "  trong mục [ " đường dẫn " ]:
				# https://www.youtube.com/channel/UC-9-kyTW8ZkZNDHQJ6FgpwQ
				yt_route =  " ytcp "  nếu  " danh sách phát "  trong mục [ " path " ] khác  " ytc "
				yt_cid = re.compile ( " youtube.com/channel/(.+?)$ " ) .findall (mục [ " đường dẫn " ]) [ 0 ]
				mục [ " path " ] =  " plugin: //plugin.video.kodi4vn.launcher/% s / % s / "  % (
					yt_route, yt_cid)
				item [ " path " ] = item [ " path " ] .replace ( " / danh sách phát " , " " )
			elif  " youtube.com/playlist "  trong mục [ " đường dẫn " ]:
				# https://www.youtube.com/playlist?list=PLFgquLnL59alCl_2TQvOiD5Vgm1hCaGSI
				yt_pid = re.compile ( " list = (. +?) $ " ) .findall (mục [ " đường dẫn " ]) [ 0 ]
				mục [ " path " ] =  " plugin: //plugin.video.kodi4vn.launcher/ytp/% s / "  % yt_pid
			elif  any (ext trong mục [ " path " ] cho ext trong [ " .png " , " .jpg " , " .bmp " , " .jpeg " ]):
				mục [ " path " ] =  " plugin: //plugin.video.kodi4vn.launcher/showimage/% s / "  % urllib.quote_plus (
					mục [ " đường dẫn " ])
			elif re.search ( " \ .ts $ " , mục [ " đường dẫn " ]):
				item [ " path " ] =  " plugin: //plugin.video.f4mTester/? url = % s & streamtype = TSDOWNLOADER & use_proxy_for_chunks = True & name = % s "  % (
					urllib.quote (mục [ " đường dẫn " ]),
					urllib.quote_plus (mục [ " nhãn " ])
				)
				mục [ " đường dẫn " ] = pluginrootpath + \
					" / execebuiltin / "  + urllib.quote_plus (mục [ " đường dẫn " ])
			khác :
				# Nếu là liên kết trực tiếp, lộ trình, vui chơi
				mục [ " is_playable " ] =  Đúng
				mục [ " thông tin " ] = { " loại " : " video " }
				mục [ " đường dẫn " ] = pluginrootpath +  " / play / "  + urllib.quote_plus (mục [ " đường dẫn " ])
		nếu mục [ " nhãn2 " ] .startswith ( " http " ):
			mục [ " đường dẫn " ] + =  " ? sub = "  + urllib.quote_plus (mục [ " nhãn2 " ] .encode ( " utf8 " ))
		mục + = [mục]
	nếu url_path ==  " 0 " :
		add_playlist_item = {
			" bối cảnh_menu " : [
				Danh sách ClearPlay ( " " ),
			],
			" nhãn " : " [MÀU màu vàng] *** Danh sách phát bổ sung *** [/ MÀU] " ,
			" đường dẫn " : " % s / add  -list " % (pluginrootpath),
			" Hình thu nhỏ " : " http://1.bp.blogspot.com/-gc1x9VtxIg0/VbggLVxszWI/AAAAAAAAANo/Msz5Wu0wN4E/s1600/playlist-advertorial.png " ,
			" is_playable " : Đúng ,
			" thông tin " : { " loại " : " video " }

		}
		mục + = [add_playlist_item]
		danh sách phát = plugin.get_st Storage ( ' danh sách phát ' )
		nếu  ' phần '  trong danh sách phát:
			cho phần trong danh sách phát [ ' phần ' ]:
				mục = {
					" bối cảnh_menu " : [
						Danh sách ClearPlay (phần),
					]
				}
				nếu  " @@ "  trong phần:
					tmp = phần.split ( " @@ " )
					passw = tmp [ - 1 ]
					phần = tmp [ 0 ]
					mục [ " nhãn " ] = phần
					mục [ " đường dẫn " ] =  " % s / phần mật khẩu / % s / % s "  % (
						pluginrootpath,
						qua đường
						phần.split ( " ] " ) [ - 1 ]
					)
				khác :
					mục [ " nhãn " ] = phần
					mục [ " đường dẫn " ] =  " % s / phần / % s "  % (
						pluginrootpath,
						phần.split ( " ] " ) [ - 1 ]
					)
				mục [ " hình thu nhỏ " ] =  " https://www.upsieutoc.com/images/2019/06/17/viuiuiuiui.png "
				mục.append (mục)
	trả lại hàng


@ plugin.route ( ' / remove-playlists / ' , name = " remove_all " )
@ plugin.route ( ' / remove-playlists / <item> ' )
def  RemovePlaylists ( item = " " ):
	mục = urllib.unquote_plus (mục)
	nếu mục không phải là  " " : 
		danh sách phát = plugin.get_st Storage ( ' danh sách phát ' )
		nếu  ' phần '  trong danh sách phát:
			new_playlists = []
			cho phần trong danh sách phát [ " phần " ]:
				nếu phần ! = mục:
					new_playlists + = [phần]
			danh sách phát [ " phần " ] = new_playlists
	khác :
		plugin.get_st Storage ( ' danh sách phát ' ) .clear ()
	xbmc.executebuiltin ( ' Container.Refresh ' )


def  ClearPlaylists ( item = " " ):
	nếu mục ==  " " :
		nhãn =  ' [MÀU màu vàng] Danh sách phát Danh sách [/ MÀU] '
	khác :
		nhãn =  ' [MÀU vàng]  Mặt hàng " % s " [/ MÀU] ' %

	return (nhãn, hành động.background (
		" % s / remove-playlists / % s "  % (pluginrootpath, urllib.quote_plus (mục))
	))


def  getValue ( colid ):
	'' '
	Hàm của họ giá trị theo
	Thông số
	----------
	colid: chuỗi
		Miền Nam
	'' '
	nếu colid không phải là  Không và colid [ " v " ] không phải là Không có :    
		trả lại colid [ " v " ]
	khác :
		trở lại  " "


@ plugin.route ( ' / ' )
def  Trang chủ ():
	''' 	Main Menu
	'' '
Theo dõi 	GA ()   #
	Mục ( " 0 " )


@ plugin.route ( ' / bộ nhớ cache / phần <path> / <theo dõi chuỗi > ' )
def  CacheedSection ( path = " 0 " , theo dõi_ chuỗi = " Trang chủ " ):
	GA (   # theo dõi
		" Mục - % s "  % theo dõi chuỗi,
		" / phần / % s "  % đường dẫn
	)
	plugin.add_sort_method (xbmcplugin. SORT_METHOD_UNSORTED )
	plugin.add_sort_method (xbmcplugin. SORT_METHOD_LABEL_IGNORE_THE )
	trả lại plugin.finish (getCachedItems (đường dẫn))


@ plugin.route ( ' / phần mật khẩu / <mật khẩu> / <đường dẫn> / <theo dõi chuỗi > ' )
def  PasswordSection ( password = " 0000 " , path = " 0 " , theo dõi_ chuỗi = " Trang chủ " ):
	'' '
	Danh sách của danh sách các mục của tấm một
	Thông số
	----------
	đường dẫn: chuỗi
		"gid" của tờ
	theo dõi chuỗi: chuỗi
		 Tên tập tin xem của
	'' '
	GA (   # theo dõi
		" Phần mật khẩu - % s "  % theo dõi chuỗi,
		" / phần mật khẩu / % s "  % đường dẫn
	)
	Mật khẩu = plugin.get_st Storage ( ' mật khẩu ' )
	plugin.add_sort_method (xbmcplugin. SORT_METHOD_UNSORTED )
	plugin.add_sort_method (xbmcplugin. SORT_METHOD_LABEL_IGNORE_THE )

	nếu mật khẩu trong mật khẩu và (time.time () - mật khẩu [mật khẩu] <  1800 ):
		mục = AddTracking (getItems (đường dẫn))
		trả lại plugin.finish (mục)
	khác :
		passw_string = plugin.keyboard ( tiêu đề = ' password Enter ' )
		if passw_opes == mật khẩu:
			mật khẩu [mật khẩu] = time.time ()
			mục = AddTracking (getItems (đường dẫn))
			trả lại plugin.finish (mục)
		khác :
			tiêu đề =  " Sảng dịch !!! "
			nhắn =  " passwords do not match. Không tải been Nội dung "
			xbmc.executebuiltin ( ' Thông báo (" % s ", " % s ", " % d ", " % s ") '  %
			                    (tiêu đề, tin nhắn, 10000 , ' ' ))
			trả lại plugin.finish ()


@ plugin.route ( ' / phần / <đường dẫn> / <theo dõi chuỗi > ' )
 Phần def ( path = " 0 " , theo dõi_ chuỗi = " Trang chủ " ):
	'' '
	Danh sách của danh sách các mục của tấm một
	Thông số
	----------
	đường dẫn: chuỗi
		"gid" của tờ
	theo dõi chuỗi: chuỗi
		 Tên tập tin xem của
	'' '
	GA (   # theo dõi
		" Mục - % s "  % theo dõi chuỗi,
		" / phần / % s "  % đường dẫn
	)
	mục = AddTracking (getItems (đường dẫn))
	plugin.add_sort_method (xbmcplugin. SORT_METHOD_UNSORTED )
	plugin.add_sort_method (xbmcplugin. SORT_METHOD_LABEL_IGNORE_THE )
	trả lại plugin.finish (mục)


@ plugin.route ( ' / add -lists / < track_opes > ' )
def  AddPlaylist ( theo dõi_ chuỗi = " Thêm danh sách phát " ):
	sheet_url = plugin.keyboard (
		đề mục = ' URL URL của Google Bảng tính (có liên kết với Google, ví dụ như bit.ly, goo.gl) ' )
	nếu sheet_url:
		nếu  không re.match ( " ^ https *: // " , sheet_url):
			sheet_url =  " https: // "  + sheet_url
		thử :
			resp, content = http.request (sheet_url, " ĐẦU " )
			sid, gid = re.compile (
				" /D/(.+?)/.+?gid=(\d+) " ) .findall (resp [ " nội dung-vị trí " ]) [ 0 ]
			match_passw = re.search ( ' passw = (. +?) ($ | &) ' , resp [ " nội dung-vị trí " ])
			danh sách phát = plugin.get_st Storage ( ' danh sách phát ' )
			Tên = plugin.keyboard ( tiêu đề = ' Set name for Danh sách phát ' )

			item =  " [[MÀU vàng] % s [/ MÀU]] % s @ % s "  % (tên, gid, sid)
			nếu match_passw:
				mục + =  " @@ "  + match_passw.group ( 1 )
			nếu  ' phần '  trong danh sách phát:
				danh sách phát [ " phần " ] = [mục] + danh sách phát [ " phần " ]
			khác :
				danh sách phát [ " phần " ] = [mục]
			xbmc.executebuiltin ( ' Container.Refresh ' )
		ngoại trừ :
			line1 =  " Please enter the URL a valid Ví examples dạng đầy đủ:. "
			line2 =  " http://docs.google.com/s Lansheet / d / xxxx /edit # gid = # # #"
			line3 =  " miền nam trên mạng : http://bit.ly/xxxxxx đường dẫn http://goo.gl/xxxxx "
			dlg = xbmcgui.Dialog ()
			dlg.ok ( " URL không kết hợp !!! " , dòng1, dòng2, dòng3)


@ plugin.route ( ' / acelist / <path> / <theo dõi_ chuỗi> ' )
def  AceList ( path = " 0 " , theo dõi_ chuỗi = " AceList " ):
	(tương ứng, nội dung) = http.request (
		đường dẫn, " NHẬN " ,
		tiêu đề = sheet_headers
	)
	vật phẩm = []
	match = re.compile ( ' <td class = "text-right"> (. +?) </ td> </ tr> <tr> <td class = "xsmall text-mute"> (. +?) < /td></tr></table></td><td>(.+?)</td>.+?href="(acestream.+?)".+?title = "(. +? ) " ' ) .findall (sạchHTML (nội dung))
	cho _time, _date, sport, aceurl, title trong trận đấu:
		title = title.strip (). split ( " <br /> " )
		title [ 0 ] =  " [MÀU vàng] % s [/ COLOR] "  % title [ 0 ]
		title =  " - " .join (tiêu đề)
		title =  " [B] [MÀU cam] % s , % s [/ MÀU] % s  % s [/ B] "  % (
			_date.strip (), re.sub ( ' <. *?> ' , ' ' , _time) .strip (), sport.strip (), tiêu đề)
		mục = {}
		mục [ " nhãn " ] = tiêu đề
		mục [ " đường dẫn " ] =  " % s / lượt chơi / % s / % s "  % (
			pluginrootpath,
			urllib.quote_plus (aceurl),
			urllib.quote_plus ( " [AceList] % s "  % item [ " nhãn " ])
		)
		mục [ " is_playable " ] =  Đúng
		mục [ " thông tin " ] = { " loại " : " video " }
		mục + = [mục]
	plugin.add_sort_method (xbmcplugin. SORT_METHOD_UNSORTED )
	plugin.add_sort_method (xbmcplugin. SORT_METHOD_LABEL_IGNORE_THE )
	trả lại plugin.finish (mục)


@ plugin.route ( ' / fshare / <path> / <theo dõi_ chuỗi > ' )
def  FShare ( path = " 0 " , theo dõi_ chuỗi = " FShare " ):
	def  toSize ( s ):
		gb =  2 ** 30
		mb =  2 ** 20
		thử :
			s =  int (s)
		ngoại trừ :
			s =  0
		nếu s > gb:
			s =  ' { : .2f } GB ' .format (s / gb)
		elif s > mb:
			s =  ' { : .0f } MB ' .format (s / mb)
		khác :
			s =  ' { : .2f } MB ' .format (s / mb)
		trở lại s
	thư mục_id = re.search ( ' thư mục / (. +?) (\? | $) ' , đường dẫn) .group ( 1 )
	trang =  1
	thử :
		page =  int (re.search ( ' page = (\ d +) ' , đường dẫn) .group ( 1 ))
	ngoại trừ :
		vượt qua
	fshare_folder_api =  " https://www.fshare.vn/api/v3/files/folder?linkcode=% s & sort = type, -modified & page = % s "  % (
		thư mục_id, trang)
	(tương ứng, nội dung) = http.request (
		fshare_folder_api, " NHẬN " ,
		tiêu đề = {
			"Tác nhân người dùng " : " Mozilla / 5.0 (Windows NT 10.0; Win64; x64) AppleWebKit / 537.36 (KHTML, như Gecko) Chrome / 72.0.3626.109 Safari / 537.36 " ,
			" Chấp nhận " : " ứng dụng / json, văn bản / đơn giản, * / * " ,
			" Chấp nhận mã hóa " : " gzip, defat, sdch, br "
		}
	)
	vật phẩm = []
	fshare_items = json.loads (nội dung) [ " mục " ]
	cho tôi trong fshare_items:
		mục = {}
		tên = i [ " tên " ] .encode ( " utf8 " )
		kích thước =  0
		thử :
			kích thước = toSize (i [ " size " ])
		ngoại trừ :
			vượt qua

		nếu  không tôi [ " loại " ]:   # là thư mục
			mục [ " đường dẫn " ] =  " % s / fshare / % s / % s "  % (
				pluginrootpath,
				urllib.quote_plus ( " https://www.fshare.vn/folder/ "  + i [ " mã liên kết " ]),
				urllib.quote_plus ( " [FShare] % s "  % name)
			)
			mục [ " nhãn " ] =  " [FShare] % s "  % name
		khác :
			mục [ " đường dẫn " ] =  " % s / lượt chơi / % s / % s "  % (
				pluginrootpath,
				urllib.quote_plus ( " https://www.fshare.vn/file/ "  + i [ " mã liên kết " ]),
				urllib.quote_plus ( " [FShare] % s ( % s ) "  % (tên, kích thước))
			)
			mục [ " nhãn " ] =  " % s ( % s ) "  % (tên, kích thước)
			mục [ " is_playable " ] =  Đúng
			mục [ " thông tin " ] = { " loại " : " video " }
		mục + = [mục]
	nếu  len (fshare_items) > =  20 :
		path =  " https://www.fshare.vn/folder/% s ? page = % s "  % (thư mục_id, trang +  1 )
		mục.append ({
			' nhãn ' : ' Tiếp theo >> ' ,
			' đường dẫn ' : ' % s / fshare / % s / % s '  % (
				pluginrootpath,
				urllib.quote_plus (đường dẫn),
				urllib.quote_plus (theo dõi)
			),
			' hình thu nhỏ ' : " https://docs.google.com/drawings/d/12OjbFr3Z5TCi1WREwTWECxNNwx0Kx-FTrCLOigrpqG4/pub?w=256&h=256 "
		})
	plugin.add_sort_method (xbmcplugin. SORT_METHOD_UNSORTED )
	plugin.add_sort_method (xbmcplugin. SORT_METHOD_LABEL_IGNORE_THE )
	trả lại plugin.finish (mục)


@ plugin.route ( ' / m3u-phần / <path> / <theo dõi_ chuỗi > ' )
def  M3USection ( path = " 0 " , theo dõi_ chuỗi = " M3U " ):
	'' '
	Danh sách danh sách các mục của bảng tính Danh sách phát M3U
	Thông số
	----------
	đường dẫn: chuỗi
		"gid" của danh sách phát M3U
	theo dõi chuỗi: chuỗi
		 Tên tập tin xem của
	'' '
	GA (   # theo dõi
		" Phần M3U - % s "  % theo dõi chuỗi,
		" / m3u-phần / % s "  % đường dẫn
	)
	mục = getItems (đường dẫn)
	cho các mục trong mục:
		# Đổi lại thành m3u mục
		mục [ " đường dẫn " ] = mục [ " đường dẫn " ] .replace ( " / play / " , " / m3u / " )
		nếu  " is_playable "  trong mục:
			mục del [ " is_playable " ]
		nếu  " có thể chơi "  trong mục:
			mục del [ " có thể chơi " ]
	plugin.add_sort_method (xbmcplugin. SORT_METHOD_UNSORTED )
	plugin.add_sort_method (xbmcplugin. SORT_METHOD_LABEL_IGNORE_THE )
	trả lại plugin.finish (AddTracking (mục))


@ plugin.route ( ' / m3u / <path> ' , name = " m3u_default " )
@ plugin.route ( ' / m3u / <path> / <theo dõi chuỗi > ' )
def  M3U ( path = " 0 " , theo dõi_ chuỗi = " M3U " ):
	'' '
	Danh sách danh sách các mục của bảng tính Danh sách phát M3U
	Thông số
	----------
	đường dẫn: chuỗi
		Liên kết danh sách nhạc trên màn hình m3u
	theo dõi chuỗi: chuỗi
		 Tên tập tin xem của
	'' '
	GA (   # theo dõi
		" M3U - % s "  % theo dõi chuỗi,
		" / m3u / % s "  % đường dẫn
	)

	mục = M3UToItems (đường dẫn)
	plugin.add_sort_method (xbmcplugin. SORT_METHOD_UNSORTED )
	plugin.add_sort_method (xbmcplugin. SORT_METHOD_LABEL_IGNORE_THE )
	trả lại plugin.finish (AddTracking (mục))


@ plugin.route ( ' / install-repo / <path> / <theo dõi_ chuỗi > ' )
def  InstallRepo ( path = " 0 " , theo dõi_ chuỗi = " " ):
	'' '
	Cài đặt repo
	Thông số
	----------
	đường dẫn: chuỗi
		Từ khóa "gid" của kho lưu trữ:
			Cài đặt tự động và repo trong bảng Kho
		Liên kết tải xuống zip repo
			Tải xuống và cài đặt zip repo tinh
	theo dõi chuỗi: chuỗi
		 Tên tập tin xem của
	'' '
	GA (   # theo dõi
		" Cài đặt Repo - % s "  % theo dõi chuỗi,
		" / install-repo / % s "  % đường dẫn
	)
	if path.itorigit (): # mộc   GID
		pDialog = xbmcgui.DialogProTHER ()
		pDialog.create ( ' Vui lòng , ' , ' cài đặt repo ' , 'Tải tải ... ' )
		mục = getItems (đường dẫn)
		tổng =  len (vật phẩm)
		i =  0
		thất bại = []
		đã cài đặt = []
		cho các mục trong mục:
			xong =  int ( 100  * i / tổng số)
			pDialog.update (đã hoàn thành, ' Gói tải ' , mục [ " nhãn " ] +  ' ... ' )
			if  " : / "  không có  trong mục [ " nhãn2 " ]:
				result = xbmc.executeJSONRPC (
					' {"jsonrpc": "2.0", "phương thức": "Addons.GetAddonDetails", "params": {"addonid": " % s ", "property": ["phiên bản"]}, "id": 1 } '  % mục [ " nhãn " ])
				json_result = json.loads (kết quả)
				nếu  " phiên bản "  trong kết quả và phiên bản_cmp (json_result [ " result " ] [ " addon " ] [ " phiên bản " ], mục [ " nhãn2 " ]) > =  0 :
					vượt qua
				khác :
					thử :
						mục [ " đường dẫn " ] =  " http "  + mục [ " đường dẫn " ] .split ( " http " ) [ - 1 ]
						tải xuống (urllib.unquote_plus (mục [ " đường dẫn " ]), mục [ " nhãn " ])
						đã cài đặt + = [item [ " nhãn " ] .encode ( " utf-8 " )]
					ngoại trừ :
						thất bại + = [mục [ " nhãn " ] .encode ( " utf-8 " )]
			khác :
				nếu  không os.path.exists (xbmc.translatePath (mục [ " nhãn2 " ])):
					thử :
						mục [ " đường dẫn " ] =  " http "  + mục [ " đường dẫn " ] .split ( " http " ) [ - 1 ]
						tải xuống (urllib.unquote_plus (mục [ " đường dẫn " ]), mục [ " nhãn2 " ])
						đã cài đặt + = [item [ " nhãn " ] .encode ( " utf-8 " )]
					ngoại trừ :
						thất bại + = [mục [ " nhãn " ] .encode ( " utf-8 " )]

			if pDialog.iscatteryed ():
				phá vỡ
			tôi + =  1
		pDialog.c Đóng ()
		nếu  len (thất bại) >  0 :
			dlg = xbmcgui.Dialog ()
			s =  " Cài đặt các ứng dụng sau: \ n [MÀU SẮC] % s [/ MÀU] "  %  " \ n " .join (
				thất bại)
			dlg.ok ( ' Chú ý: Không gian repo! ' , s)
		khác :
			dlg = xbmcgui.Dialog ()
			s =  " Toàn bộ repo và cài đặt thành công \ n % s "  %  " \ n " .join (đã cài đặt)
			dlg.ok ( ' Cài Repo thành công! ' , s)

	khác :   # cài đặt lại
		thử :
			tải xuống (đường dẫn, " " )
			dlg = xbmcgui.Dialog ()
			s =  " Repo % s have installed successfully "  % tracking_string
			dlg.ok ( ' Cài Repo thành công! ' , s)
		ngoại trừ :
			dlg = xbmcgui.Dialog ()
			s =  " Vùi chiếm chỗ cài đặt lại sau "
			dlg.ok ( ' Cài đặt lại trò chơi! ' , s)

	xbmc.executebuiltin ( " XBMC.UpdateLocalAddons () " )
	xbmc.executebuiltin ( " XBMC.UpdateAddonRepos () " )


@ plugin.route ( ' / repo-phần / <path> / <theo dõi_ chuỗi > ' )
def  RepoSection ( path = " 0 " , theo dõi_ chuỗi = " " ):
	'' '
	Repo sao kê repo
	Thông số
	----------
	đường dẫn: chuỗi
		Liên kết tải xuống zip repo.
	theo dõi chuỗi: chuỗi
		Tên tập tin xem của
	'' '
	GA (   # theo dõi
		" Phần Repo - % s "  % theo dõi chuỗi,
		" / repo-phần / % s "  % đường dẫn
	)

	mục = getItems (đường dẫn)
	cho các mục trong mục:
		if  " / play / "  trong mục [ " path " ]:
			item [ " path " ] = item [ " path " ] .replace ( " / play / " , " / install-repo / " )
		# hack mục xbmcswift2 để đặt cả is_playable và is_folder thành Sai
		mục [ " is_playable " ] =  Sai
	các mặt hàng = AddTracking (các mặt hàng)

	install_all_item = {
		" nhãn " : " [MÀU màu xanh lá cây] Tự động cài đặt cả Repo, (tính năng) [/ MÀU] " .decode ( " utf-8 " ),
		" path " : pluginrootpath +  " / install-repo / % s / % s "  % (path, urllib.quote_plus ( " Cài đặt tất cả repo " )),
		" is_playable " : Sai ,
		" thông tin " : { " cốt truyện " : " Bạn có thể sử dụng toàn bộ phần thưởng của bạn [phần mở rộng của danh sách [VN Open Playlist] " }
	}
	vật phẩm = [install_all_item] + vật phẩm
	trả lại plugin.finish (mục)


 tải xuống def ( download_path , repo_id ):
	'' '
	Thông số
	----------
	đường dẫn: chuỗi
		Liên kết tải xuống zip repo.
	repo_id: chuỗi
		Tên của chúng tôi repo
		Mang tên phần mềm cho mục ["nhãn2"].
		Truyền "
	'' '
	nếu repo_id ==  " " :
		repo_id =  " tạm thời "
	nếu  " : / "  không có  trong repo_id:
		zipfile_path = xbmc.transTablePath (os.path.join (tmp, " % s .zip "  % repo_id))
		urllib.urlretrieve (download_path, zipfile_path)
		với zipfile.ZipFile (zipfile_path, " r " ) là z:
			z.extractall (addons_folder)
	khác :
		zipfile_path = xbmc.transTablePath (
			os.path.join (tmp, " % s .zip "  % repo_id.split ( " / " ) [ - 1 ]))
		urllib.urlretrieve (download_path, zipfile_path)
		với zipfile.ZipFile (zipfile_path, " r " ) là z:
			z.extractall (xbmc.translatePath ( " / " .join (repo_id.split ( " / " ) [: - 1 ])))


def  AddTracking ( mục ):
	'' '
	Theo dõi hàm góc cho các mục
	Thông số
	----------
	mục: danh sách
		Danh sách các mặt hàng theo cuốn sách xbmcswift2.
	'' '

	cho các mục trong mục:
		nếu  " plugin.video.tranhuyhoang.playlist "  trong mục [ " path " ]:
			tmps = item [ " đường dẫn " ] .split ( " ? " )
			nếu  len (tmps) ==  1 :
				đuôi =  " "
			khác :
				đuôi = tmps [ 1 ]
			mục [ " path " ] =  " % s / % s ? % s "  % (tmps [ 0 ], urllib.quote_plus (mục [ " nhãn " ]), đuôi)
	trả lại hàng


@ plugin.route ( ' / showimage / <url> / <theo dõi chuỗi> ' )
def  showimage ( url , theo dõi chuỗi ):
	xbmc.executebuiltin ( " ShowPicture ( % s ) "  % urllib.unquote_plus (url))


@ plugin.route ( ' / execebuiltin / <path> / <theo dõi_ chuỗi> ' )
def  execbuiltin ( path , theo dõi_ chuỗi = " " ):
	GA (   # theo dõi
		" Thực thi nội dung - % s "  % theo dõi chuỗi,
		" / repo-execbuiltin / % s "  % đường dẫn
	)
	thử :
		xbmc.executebuiltin ( ' XBMC.RunPlugin ( % s ) '  % urllib.unquote_plus (đường dẫn))
	ngoại trừ :
		vượt qua


@ plugin.route ( ' / play / <url> / <title> ' )
def  play_url ( url , title = " " ):
	GA ( " Phát [ % s ] "  % title, " / play / % s / % s "  % (title, url))
	url = get_playable_url (url)
	# Hack cho một số liên kết chuyển hướng lỗi
	thử :
		http = httplib2.Http ( disable_ssl_certificate_validation = Đúng )
		http.follow_redirects =  Đúng
		(tương ứng, nội dung) = http.request (
			url, " ĐẦU "
		)
		url = resp [ ' nội dung-vị trí ' ]
	ngoại trừ :
		vượt qua
	nếu  " phụ "  trong plugin.request.args:
		plugin.set_resolve_url (url, phụ đề = plugin.request.args [ " sub " ] [ 0 ])
	khác :
		plugin.set_resolve_url (url)


def  get_playable_url ( url ):
	nếu  " youtube "  trong url:
		khớp = re.compile (
			' (youtu \ .be \ / | youtube-nocookie \ .com \ / | youtube \ .com \ / (xem \? (. * &)? v = | (nhúng | v | người dùng) \ /)) ([ ^ \? & " \ ' >] +) ' ) .findall (url)
		yid = trận đấu [ 0 ] [ len (trận đấu [ 0 ]) - 1 ] .replace ( ' v / ' , ' ' )
		url =  ' plugin: //plugin.video.youtube/play/? video_id = % s '  % yid
	elif  " thvli.vn/backend/cm/detail/ "  trong url:
		get_thvl =  " https://docs.google.com/spreadsheets/d/13VzQebjGYac5hxe1I-z1pIvMiNB0gSG7oWJlFHWnqsA/export?format=tsv&gid=1287121588 "
		thử :
			(tương ứng, nội dung) = http.request (
				get_thvl, " NHẬN "
			)
		ngoại trừ :
			tiêu đề =  " Máy chủ tải! "
			tin nhắn =  " Xin vui lòng tải lại sau "
			xbmc.executebuiltin ( ' Thông báo (" % s ", " % s ", " % d ", " % s ") '  %
			                    (tiêu đề, tin nhắn, 10000 , ' ' ))
			trở lại  " "

		tmps = content.split ( ' \ n ' )
		ngẫu nhiên.shuffle (tmps)
		cho tmp trong tmps:
			thử :
				thvl_headers = {
					'Tác nhân người dùng ' : ' Mozilla / 5.0 (tương thích; MSIE 10.0; Windows NT 6.3; WOW64; Trident / 7.0) ' ,
					" Chấp nhận mã hóa " : " gzip, deflate, br " ,
					' Chấp nhận ' : ' ứng dụng / json ' ,
					' Ủy quyền ' : tmp.decode ( ' base64 ' )
				}

				(tương ứng, nội dung) = http.request (
					url, " NHẬN " , tiêu đề = thvl_headers
				)
				resp_json = json.loads (nội dung)
				nếu  " link_play "  trong resp_json:
					trả về resp_json [ " link_play " ]
			ngoại trừ :
				vượt qua
	elif  " sphim.tv "  trong url:
		http.follow_redirects =  Sai
		get_sphim =  " https://docs.google.com/spreadsheets/d/13VzQebjGYac5hxe1I-z1pIvMiNB0gSG7oWJlFHWnqsA/export?format=tsv&gid=1082544232 "
		thử :
			(tương ứng, nội dung) = http.request (
				get_sphim, " NHẬN "
			)
		ngoại trừ :
			tiêu đề =  " Máy chủ tải! "
			tin nhắn =  " Xin vui lòng tải lại sau "
			xbmc.executebuiltin ( ' Thông báo (" % s ", " % s ", " % d ", " % s ") '  %
			                    (tiêu đề, tin nhắn, 10000 , ' ' ))
			trở lại  " "

		tmps = content.split ( ' \ n ' )
		ngẫu nhiên.shuffle (tmps)
		cho tmp trong tmps:
			thử :
				sphim_headers = {
					'Tác nhân người dùng ' : ' Mozilla / 5.0 (Windows NT 10.0; Win64; x64) AppleWebKit / 537.36 (KHTML, như Gecko) Chrome / 59.0.3071.115 Safari / 537.36 ' ,
					" Mã hóa chấp nhận " : " gzip, giảm phát " ,
					' Cookie ' : tmp.decode ( " cơ sở64 " )
				}

				(tương ứng, nội dung) = http.request (
					url, " NHẬN " , tiêu đề = sphim_headers
				)
				khớp = re.search ( ' "(http. +? \. smil /lists.m3u8. +?)" ' , nội dung)
				nếu khớp
					trả lại trận đấu. nhóm ( 1 )
			ngoại trừ :
				vượt qua
	elif url.startswith ( " acestream: // " ) hoặc url.endswith ( " .acelive " ) hoặc  " arenavision.in "  trong url:
		nếu  " arenavision.in "  trong url:
			h = {
				'Tác nhân người dùng ' : ' Mozilla / 5.0 (Windows NT 10.0; WOW64) AppleWebKit / 537.36 (KHTML, như tắc kè) Chrome / 47.0.2526.106 Safari / 537.36 ' ,
				' Cookie ' : ' __cfduid = d36d59e9714c527d920417ed5bbc9315e1496259947; beget = begetok; ads_smrt_popunder = 1% 7CSat% 2C % 2003% 20Jun % 202017% 2018% 3A57% 3A05 % 20G MT; 141054_245550_1rhpmin = có; 141054_245550_1rhpmax = 4 | Sat% 2C % 2003% 20Jun % 202017% 2018% 3A57% 3A14 % 20G MT; has_js = 1; _ga = GA1.2.652127938.1496259947; _gid = GA1.2,653920302.1496429805; _gat = 1 ' ,
				' Chấp nhận mã hóa ' : ' gzip, giảm phát '
			}
			(tương ứng, nội dung) = http.request (
				url,
				" NHẬN " , tiêu đề = h
			)
			url = re.search ( ' (acestream: //.+?) " ' , nội dung) .group ( 1 )
		thử :
			(tương ứng, nội dung) = http.request (
				" http: // localhost: 6878 / webui / api / dịch vụ " ,
				" TRỤ "
			)
			url = url.replace (
				" acestream: // " , " http: // localhost: 6878 / ace / getstream? id = " ) +  " & .mp4 "
			nếu url.endswith ( " .acelive " ):
				url =  " http: // localhost: 6878 / ace / getstream? url = "  + \
					urllib.quote_plus (url) +  " & .mp4 "
		ngoại trừ :
			url =  ' plugin: //program.plexus/? url = % s & mode = 1 & name = P2PStream & iconimage = '  % urllib.quote_plus (
				url)
	elif  any (tên miền trong url cho tên miền trong [ " m.tivi8k.net " , " m.xemtvhd.com " , " xem activiso.com " ]):
		play_url =  " "
		nếu  " xem activiso.com "  không có  trong url:
			cho tôi trong  phạm vi ( 1 , 8 ):
				thử :
					nếu tôi >  1 :
						phạm vi_url = url.replace ( " .php " , " - % s .php "  % i)
					h1 = {
						'Tác nhân người dùng ' : ' Mozilla / 5.0 (Windows NT 10.0; Win64; x64) AppleWebKit / 537.36 (KHTML, như Gecko) Chrome / 59.0.3071.115 Safari / 537.36 ' ,
						' Chấp nhận mã hóa ' : ' gzip, giảm phát ' ,
						'Người giới thiệu ' : ' % s '  % url.replace ( " / m. " , " / Www. " )
					}
					(tương ứng, nội dung) = http.request (
						phạm vi_url,
						" NHẬN " , tiêu đề = h1,
					)
					content = content.replace ( " ' " , ' " ' )

					thử :
						play_url = re.search ( " https *: //api.tivi8k.net/.+? ' " , nội dung) .group ( 1 )
						(tương ứng, nội dung) = http.request (
							phạm vi_url,
							" NHẬN " , tiêu đề = h1,
						)
						nếu  " # EXTM3U "  trong nội dung:
							trở lại play_url
						khác :
							trả về nội dung.strip ()
					ngoại trừ :
						vượt qua
					play_url = play_url.replace ( " q = trung bình " , " q = cao " )
					nếu  " v4live "  trong play_url:
						trở lại play_url
				ngoại trừ :
					vượt qua
			thử :
				xem activiso_id = re.search ( " /(.+?).php " , url) .group ( 1 ) .split ( " - " ) [ 0 ]
				xem activiso_url =  " http :  //sv2.xem activiso.com/mimi.php?id= " + xem activiso_id
				h1 = {
					'Tác nhân người dùng ' : ' Mozilla / 5.0 (Windows NT 10.0; Win64; x64) AppleWebKit / 537.36 (KHTML, như Gecko) Chrome / 59.0.3071.115 Safari / 537.36 ' ,
					' Chấp nhận mã hóa ' : ' gzip, giảm phát ' ,
					'Người giới thiệu ' : ' % s '  % xem activiso_url
				}
				(tương ứng, nội dung) = http.request (
					xem activiso_url,
					" NHẬN " , tiêu đề = h1,
				)
				content = content.replace ( " ' " , ' " ' )
				play_url = re.search ( ' nguồn \: "(. +?)" ' , nội dung) .group ( 1 )
				play_url = play_url.replace ( " q = trung bình " , " q = cao " )
				nếu  " v4live "  trong play_url:
					trở lại play_url
			ngoại trừ :
				vượt qua
		khác :
			thử :
				h1 = {
					'Tác nhân người dùng ' : ' Mozilla / 5.0 (Windows NT 10.0; Win64; x64) AppleWebKit / 537.36 (KHTML, như Gecko) Chrome / 59.0.3071.115 Safari / 537.36 ' ,
					' Chấp nhận mã hóa ' : ' gzip, giảm phát ' ,
					'Người giới thiệu ' : ' % s '  % url.replace ( " / m. " , " / Www. " )
				}
				(tương ứng, nội dung) = http.request (
					url,
					" NHẬN " , tiêu đề = h1,
				)
				content = content.replace ( " ' " , ' " ' )
				play_url = re.search ( ' nguồn \: "(. +?)" ' , nội dung) .group ( 1 )
				play_url = play_url.replace ( " q = trung bình " , " q = cao " )
			ngoại trừ :
				vượt qua
		trở lại play_url
	elif  " vtc.gov.vn "  trong url:
		tiêu đề = {
			'Tác nhân người dùng ' : ' Mozilla / 5.0 (Windows NT 10.0; Win64; x64) AppleWebKit / 537.36 (KHTML, như Gecko) Chrome / 69.0.3497.92 Safari / 537.36 ' ,
			' Chấp nhận mã hóa ' : ' Không '
		}
		(tương ứng, nội dung) = http.request (
			url,
			" NHẬN " ,
			tiêu đề = tiêu đề
		)
		khớp = re.search ( " src: '(. +?)' " , nội dung)
		trả lại trận đấu. nhóm ( 1 )
	elif  " livestream.com "  trong url:
		tiêu đề = {
			'Tác nhân người dùng ' : ' Mozilla / 5.0 (Windows NT 10.0; WOW64; rv: 48.0) Tắc kè / 20100101 Firefox / 48.0 ' ,
			' Chấp nhận mã hóa ' : ' gzip, giảm phát ' ,
		}
		thử :
			nếu  " sự kiện "  không có  trong url:
				(tương ứng, nội dung) = http.request (
					url,
					" NHẬN " , tiêu đề = tiêu đề,
				)
				khớp = re.search ( " tài khoản / \ d + / sự kiện / \ d + " , nội dung)
				url =  " https://livestream.com/api/% s "  % match.group ()
			(tương ứng, nội dung) = http.request (
				url,
				" NHẬN " , tiêu đề = tiêu đề,
			)
			j = json.loads (nội dung)
			url = j [ " stream_info " ] [ " m3u8_url " ]
		ngoại trừ :
			vượt qua
	elif  " onecloud.media "  trong url:
		ocid = url.split ( " / " ) [ - 1 ] .strip ()
		oc_url =  " http://onecloud.media/embed/ "  + ocid
		h = {
			'Tác nhân người dùng ' : ' Mozilla / 5.0 (Windows NT 10.0; Win64; x64) AppleWebKit / 537.36 (KHTML, như Gecko) Chrome / 58.0.3029.96 Safari / 537.36 ' ,
			' Chấp nhận mã hóa ' : ' gzip, def def, sdch ' ,
			' Loại nội dung ' : ' application / x-www-form-urlencoding; bộ ký tự = UTF-8 ' ,
			' X-Requested-With ' : ' XMLHttpRequest ' ,
			' Cookie ' : ' TimeOut = 999999999 ' }
		(tương ứng, nội dung) = http.request (
			tháng tám,
			" BÀI " , tiêu đề = h,
			body = urllib.urlencode ({ ' loại ' : ' directLink ' , ' ip ' : ' ' })
		)

		thử :
			url = json.loads (nội dung) [ " list " ] [ 0 ] [ " file " ]
		ngoại trừ :
			tiêu đề =  " Có lỗi ra ra! "
			nhắn =  " Unable to fetch link been (liên kết hỏng or deleted) "
			xbmc.executebuiltin ( ' Thông báo (" % s ", " % s ", " % d ", " % s ") '  % (tiêu đề, tin nhắn, 10000 , ' ' ))
			trở lại  " "
	elif  " pscp.tv "  trong url:
		pscpid = re.search ( " w /(.+?)($ | \?) " , url) .group ( 1 )
		api_url =  " https://proxsee.pscp.tv/api/v2/accessVideoPublic?broadcast_id=% s & replay_redirect = false "  % pscpid
		(tương ứng, nội dung) = http.request (
			api_url,
			" NHẬN "
		)
		trả về json.loads (nội dung) [ " hls_url " ]
	elif  " google.com "  trong url:
		url = getGDriveHighestQuality (url)
	elif re.match ( " ^ https * \: // www \ .fshare \ .vn / file " , url):
		thử :
			tín dụng = GetFShareCred ()
			nếu tín dụng:
				fshare_headers = {
					" Chấp nhận mã hóa " : " gzip, deflate, br " ,
					' Cookie ' : ' session_id = % s '  % credit [ " session_id " ]
				}
				dữ liệu = {
					" url " : url,
					" mã thông báo " : tín dụng [ " mã thông báo " ],
					" mật khẩu " : " "
				}

				(tương ứng, nội dung) = http.request (
					convert_ipv4_url ( " https://api2.fshare.vn/api/session/doad " ), " POST " ,
					cơ thể = json.dumps (dữ liệu),
					tiêu đề = fshare_headers
				)
				url = json.loads (nội dung) [ " vị trí " ]
				url = convert_ipv4_url (url)
				nếu resp.status ==  404 :
					tiêu đề =  " Liên kết Quảng cáo VIP FShare VIP! "
					nhắn =  " Liên kết do not exist or tập have been to delete "
					xbmc.executebuiltin ( ' Thông báo (" % s ", " % s ", " % d ", " % s ") '  % (tiêu đề, tin nhắn, 10000 , ' ' ))
					trở về  Không
				(tương ứng, nội dung) = http.request (
					url, " ĐẦU "
				)
				if  ' / ERROR '  in resp [ ' content-location ' ]:
					tiêu đề =  " Liên kết Quảng cáo VIP FShare VIP! "
					nhắn =  " Liên kết do not exist or tập have been to delete "
					xbmc.executebuiltin ( ' Thông báo (" % s ", " % s ", " % d ", " % s ") '  % (tiêu đề, tin nhắn, 10000 , ' ' ))
					trở về  Không
				url trả về
			trở về  Không
		ngoại trừ :	 vượt qua
	elif  " tv24.vn "  trong url:
		cid = re.compile ( ' / (\ d +) / ' ) .findall (url) [ 0 ]
		trả về  " plugin: //plugin.video.sctv/play/ "  + cid
	elif  " dailymotion.com "  trong url:
		did = re.compile ( " / (\ w +) $ " ) .findall (url) [ 0 ]
		trả về  " plugin: //plugin.video.dailymotion_com/? url = % s & mode = playVideo "  % đã làm
	khác :
		nếu  " : // "  không có  trong url:
			url =  Không có
	url trả về

def  convert_ipv4_url ( url ):
	máy chủ = re.search ( ' //(.+?)(/ | \ :) ' , url) .group ( 1 )
	addrs = socket.getaddrinfo (máy chủ, 443 )
	ipv4_addrs = [addr [ 4 ] [ 0 ] cho addr trong addrs nếu addr [ 0 ] == socket. SAU ]
	url = url.replace (máy chủ, ipv4_addrs [ 0 ])
	url trả về

def  Đăng nhậpFShare ( uname , pword ):
	login_uri =  " https://api2.fshare.vn/api/user/login "
	login_uri = convert_ipv4_url (login_uri)
	fshare_headers = {
		"Tác nhân người dùng " : " Mozilla / 5.0 (Windows NT 6.1; Win64; x64) AppleWebKit / 537.36 (KHTML, như Gecko) Chrome / 68.0.3440.106 Safari / 537.36 " ,
		" Chấp nhận mã hóa " : " gzip, giảm phát, sdch "
	}
	data =  ' {"app_key": "L2S7R6ZMagggC5wWkQhX2 + aDi467PPuftWUMRFSn", "user_email": " % s ", "password": " % s "} '  % (uname, pword)
	resp, cont = http.request (login_uri, " POST " , headers = fshare_headers, body = data)
	nếu  " mã thông báo "  trong tiếp và  " session_id "  trong tiếp:
		plugin.set_setting ( " tín dụng " , tiếp)
		plugin.set_setting ( " băm " , uname + pword)
		_json = json.loads (tiếp)
		trở lại _json
	khác : trả lại  Không

def  get_fshare_setting ( s ):
	thử :
		trả lại plugin.get_setting (s)
	ngoại trừ : trả lại  " "

def  GetFShareCred ():
	thử :
		_hash = get_fshare_setting ( " băm " )
		uname = get_fshare_setting ( " tên người dùng " )
		pword = get_fshare_setting ( " passwordfshare " )
		if _hash ! = (uname + pword):
			plugin.set_setting ( " tín dụng " , " " )
		tín dụng   = json.loads (get_fshare_setting ( " tín dụng " ))
		người dùng = GetFShareUser (tín dụng)
		Đăng nhậpOKNoti (người dùng [ " email " ], người dùng [ " cấp " ])
		trả lại tín dụng
	ngoại trừ :
		thử :
			uname = get_fshare_setting ( " tên người dùng " )
			pword = get_fshare_setting ( " passwordfshare " )
			tín dụng = Đăng nhậpFShare (uname, pword)
			người dùng = GetFShareUser (tín dụng)
			Đăng nhậpOKNoti (người dùng [ " email " ], người dùng [ " cấp " ])
			trả lại tín dụng
		ngoại trừ :
			hộp thoại = xbmcgui.Dialog ()
			có = hộp thoại.yesno (
				' Đăng nhập không thành công! \ n ' ,
				' [COLOR vàng] Bạn muốn nhập Account Fshare VIP now is not? [/ COLOR] ' ,
				yeslabel = ' OK, khỏe ngay ' ,
				nolabel = ' Bỏ qua '
			)
			nếu có:
				plugin.open_sinstall ()
				trả về GetFShareCred ()
			trở về  Không


def  Đăng nhậpOKNoti ( user = " " , lvl = " " ):
	tiêu đề =  " [MÀU vàng] Đăng ký thành công! [/ MÀU] "
	message =  " Chào [MÀU màu đỏ] VIP [/ MÀU] [MÀU SẮC] {} [/ MÀU] (lvl [MÀU màu vàng] {} [/ MÀU]) " .format (người dùng, lvl)
	xbmc.executebuiltin ( ' Thông báo (" {} ", " {} ", " {} ", "") ' .format (tiêu đề, tin nhắn, " 10000 " ))


def  GetFShareUser ( tín dụng ):
	user_url =  " https://api2.fshare.vn/api/user/get "
	user_url = convert_ipv4_url (user_url)
	tiêu đề = {
		" Cookie " : " session_id = "  + credit [ " session_id " ]
	}
	resp, cont = http.request (user_url, " GET " , tiêu đề = tiêu đề)
	người dùng = json.loads (tiếp)
	người dùng trở lại


def  GetPlayLinkFromDriveID ( drive_id ):
	play_url =  " https://drive.google.com/uc?export=mp4&id=% s "  % drive_id
	(tương ứng, nội dung) = http.request (
		play_url, " ĐẦU " ,
		tiêu đề = sheet_headers
	)
	xác nhận =  " "
	thử :
		xác nhận = re.compile (
			' download_warning _. +? = (. +?); ' ) .findall (resp [ ' set-cookie ' ]) [ 0 ]
	ngoại trừ :
		trở lại play_url
	tail =  " | Tác nhân người dùng = % s & Cookie = % s "  % (urllib.quote (
		sheet_headers [ "Tác nhân người dùng " ]), urllib.quote (resp [ ' set-cookie ' ]))
	play_url =  " % s & xác nhận = % s "  % (play_url, xác nhận) + đuôi
	trở lại play_url


def  GA ( title = " Trang chủ " , trang = " / " ):
	'' '
	Hàm của chúng tôi sử dụng Google Analytics (GA)
	Thông số
	----------
	tiêu đề: chuỗi
		Tên tin tưởng xem của.
	trang: chuỗi
		Quan điểm của hướng dẫn.
	'' '
	thử :
		ga_url =  " http://www.google-analytics.com/collect "
		client_id =  mở (cid_path) .read ()
		dữ liệu = {
			' v ' : ' 1 ' ,
			' tid ' : ' UA-52209804-5 ' ,   # Thay GA id của bạn ở
			' cid ' : client_id,
			' t ' : ' số lần xem trang ' ,
			Trang ' dp ' : " VNPlaylist % s "  % ,
			' dt ' : " [VNPlaylist] - % s "  % title
		}
		http.request (
			ga_url, " BÀI ĐĂNG " ,
			cơ thể = urllib.urlencode (dữ liệu)
		)
	ngoại trừ :
		vượt qua


def  getGDriveHighestQuality ( url ):
	(tương ứng, nội dung) = http.request (
		url, " NHẬN " ,
		tiêu đề = sheet_headers
	)
	match = re.compile ( ' (\ ["fmt_stream_map". +? \]) ' ) .findall (nội dung) [ 0 ]
	prefer_quality = [ " 38 " , " 37 " , " 46 " , " 22 " , " 45 " , " 18 " , " 43 " ]
	stream_map = json.loads (khớp) [ 1 ] .split ( " , " )
	cho q trong prefer_quality:
		cho luồng trong stream_map:
			if stream.startswith (q + " | " ):
				url = stream.split ( " | " ) [ 1 ]
				tail =  " | Tác nhân người dùng = % s & Cookie = % s "  % (urllib.quote (
					sheet_headers [ "Tác nhân người dùng " ]), urllib.quote (resp [ ' set-cookie ' ]))
				trả lại url + đuôi


def  sạchHTML ( s ):
	s =  ' ' .join (s.splitlines ()). thay thế ( ' \' ' , ' " ' )
	s = s.replace ( ' \ n ' , ' ' )
	s = s.replace ( ' \ t ' , ' ' )
	s = re.sub ( '   + ' , '  ' , s)
	s = s.replace ( ' > < ' , ' > < ' )
	trở lại s


def  phiên bản_cmp ( local_version , download_version ):
	def  bình thường hóa ( v ):
		return [ int (x) cho x trong re.sub ( r ' ( \. 0 + ) * $ ' , ' ' , v) .split ( " . " )]
	trả về  cmp (chuẩn hóa (local_version), chuẩn hóa (download_version))


# Id khách hàng id theo dõi GA
# Tham ảo ứng dụng khách id tại https://support.google.com/analyticsaru/6205850?hl=vi
device_path = xbmc.translatePath ( ' đặc biệt: // userdata ' )
if os.path.exists (device_path) ==  Sai :
	os.mkdir (device_path)
cid_path = os.path.join (device_path, ' cid ' )
if os.path.exists (cid_path) ==  Sai :
	với  mở (cid_path, " w " ) là f:
		f.write ( str (uuid.uuid1 ()))
if  __name__  ==  ' __main__ ' :
	plugin.run ()
