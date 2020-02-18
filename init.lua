local http = minetest.request_http_api()

minetest.register_globalstep(function(dtime)

	http.fetch({
		url = 'http://localhost:2468/code/get'
	}, function(resp)
		local payload = minetest.parse_json(resp.data)
		if payload then
			for i = 1, #payload do
				eval(payload[i].code)
			end end
	end)

end)

function errhandler(e)
	minetest.debug('reploops' .. dump(e))
end

function eval(s)
	minetest.debug('calling ' .. s)
	local fn = loadstring(s)
	xpcall(fn, errhandler)
end
