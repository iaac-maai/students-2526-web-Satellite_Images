import os
import argparse
import pathlib
import requests

print(">>> fetch_tile.py is running")

# Default configuration
DEFAULT_ZOOM = 18
DEFAULT_WIDTH = 512
DEFAULT_HEIGHT = 512
DEFAULT_STYLE = "satellite-v9"  # Mapbox style id

def build_mapbox_url(lon: float, lat: float, token: str,
                     zoom: int = DEFAULT_ZOOM,
                     width: int = DEFAULT_WIDTH,
                     height: int = DEFAULT_HEIGHT,
                     style: str = DEFAULT_STYLE) -> str:
    """
    Build the Mapbox Static Images API URL for a single tile.
    Centered at (lon, lat) with given zoom and size.
    """
    base = f"https://api.mapbox.com/styles/v1/mapbox/{style}/static"
    # center is LON,LAT,ZOOM
    center = f"{lon},{lat},{zoom}"
    size = f"{width}x{height}"
    url = f"{base}/{center}/{size}?access_token={token}"
    return url

def download_image(url: str, output_path: pathlib.Path) -> None:
    print(">>> Starting HTTP request...")  # DEBUG
    response = requests.get(url, stream=True, timeout=20)  # 20s timeout
    print(f">>> HTTP status code: {response.status_code}")  # DEBUG
    response.raise_for_status()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
    print(">>> Finished writing file")  # DEBUG

def main():
    print(">>> main() started")  # DEBUG

    parser = argparse.ArgumentParser(
        description="Download a Mapbox satellite image for given coordinates."
    )
    parser.add_argument("--lat", type=float, required=True, help="Latitude")
    parser.add_argument("--lon", type=float, required=True, help="Longitude")
    parser.add_argument("--zoom", type=int, default=DEFAULT_ZOOM, help="Zoom level (default 18)")
    parser.add_argument("--width", type=int, default=DEFAULT_WIDTH, help="Image width in pixels (default 512)")
    parser.add_argument("--height", type=int, default=DEFAULT_HEIGHT, help="Image height in pixels (default 512)")
    parser.add_argument("--style", type=str, default=DEFAULT_STYLE, help="Mapbox style id (default satellite-v9)")
    parser.add_argument("--outdir", type=str, default="output", help="Output folder")

    args = parser.parse_args()
    print(f">>> Parsed args: lat={args.lat}, lon={args.lon}")  # DEBUG

    token = os.environ.get("MAPBOX_TOKEN")
    print(f">>> MAPBOX_TOKEN present? {bool(token)}")  # DEBUG
    if not token:
        raise SystemExit(
            "ERROR: MAPBOX_TOKEN environment variable not set.\n"
            "Set it to your Mapbox access token and run again."
        )

    url = build_mapbox_url(
        lon=args.lon,
        lat=args.lat,
        token=token,
        zoom=args.zoom,
        width=args.width,
        height=args.height,
        style=args.style,
    )

    print(f">>> Requesting image from:\n{url}\n")  # DEBUG

    # File name like: lat_40_4168_lon_-3_7038_z_18.png
    safe_lat = str(args.lat).replace(".", "_")
    safe_lon = str(args.lon).replace(".", "_")
    filename = f"lat_{safe_lat}_lon_{safe_lon}_z_{args.zoom}.png"

    outdir = pathlib.Path(args.outdir)
    output_path = outdir / filename

    print(f">>> Output will be saved to: {output_path}")  # DEBUG
    download_image(url, output_path)
    print(f">>> Done! Saved image to: {output_path.resolve()}")


    # File name like: lat_40.12345_lon_-3.12345_zoom_18.png
    safe_lat = str(args.lat).replace(".", "_")
    safe_lon = str(args.lon).replace(".", "_")
    filename = f"lat_{safe_lat}_lon_{safe_lon}_z_{args.zoom}.png"

    outdir = pathlib.Path(args.outdir)
    output_path = outdir / filename

    print(f"Requesting image from:\n{url}\n")
    download_image(url, output_path)
    print(f"Saved image to: {output_path.resolve()}")

if __name__ == "__main__":
    main()