TOPDIR:=$(shell pwd)

create-%:
	@sed -e "s/{name_page}/yolo/g" ${TOPDIR}/base/scraper_base.py > scraper_$(subst create-,,$@).py
